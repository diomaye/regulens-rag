"""Download PDFs from manifest URLs and verify SHA-256 hashes."""

from __future__ import annotations

import hashlib
import logging
from typing import TYPE_CHECKING

import httpx

if TYPE_CHECKING:
    from pathlib import Path

    from regulens.manifest import ManifestRow

logger = logging.getLogger(__name__)


def sha256_file(path: Path) -> str:
    """Compute the SHA-256 hex digest of a file."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def download_document(
    row: ManifestRow,
    dest_dir: Path,
    *,
    timeout: float = 60.0,
    overwrite: bool = False,
) -> Path:
    """Download a single PDF and verify its hash.

    Returns the path to the downloaded file.
    Raises ``HashMismatchError`` if the SHA-256 doesn't match.
    """
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / f"{row.doc_id}.pdf"

    if dest.exists() and not overwrite:
        actual = sha256_file(dest)
        if row.sha256 and actual != row.sha256:
            msg = (
                f"{row.doc_id}: existing file hash {actual[:12]}... "
                f"!= manifest {row.sha256[:12]}..."
            )
            raise HashMismatchError(msg)
        logger.info("Skipping %s (already downloaded)", row.doc_id)
        return dest

    logger.info("Downloading %s from %s", row.doc_id, row.url)
    with httpx.Client(timeout=timeout, follow_redirects=True) as client:
        resp = client.get(row.url)
        resp.raise_for_status()

    dest.write_bytes(resp.content)

    actual = sha256_file(dest)
    if row.sha256 and actual != row.sha256:
        dest.unlink()
        msg = f"{row.doc_id}: downloaded hash {actual[:12]}... != manifest {row.sha256[:12]}..."
        raise HashMismatchError(msg)

    logger.info("Downloaded %s (%d bytes, sha256=%s)", row.doc_id, len(resp.content), actual[:12])
    return dest


class HashMismatchError(Exception):
    """Raised when a downloaded file's SHA-256 doesn't match the manifest."""
