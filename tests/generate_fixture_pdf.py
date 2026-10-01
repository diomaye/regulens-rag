"""Generate a tiny 2-page fixture PDF for testing. Run once."""

from pathlib import Path

import pymupdf

OUTPUT = Path(__file__).parent / "fixtures" / "sample.pdf"


def main() -> None:
    doc = pymupdf.open()

    # Page 1
    page1 = doc.new_page(width=612, height=792)
    page1.insert_text((72, 72), "SAMPLE GUIDELINE", fontsize=16)
    page1.insert_text((72, 110), "1. Introduction", fontsize=14)
    page1.insert_text(
        (72, 140),
        "This guideline sets out expectations for financial institutions\n"
        "regarding model risk management. Institutions should maintain\n"
        "a comprehensive model inventory.",
        fontsize=11,
    )
    page1.insert_text((72, 220), "1.1. Scope", fontsize=13)
    page1.insert_text(
        (72, 250),
        "This section applies to all federally regulated financial\n"
        "institutions (FRFIs) in Canada.",
        fontsize=11,
    )

    # Page 2
    page2 = doc.new_page(width=612, height=792)
    page2.insert_text((72, 72), "2. Definitions", fontsize=14)
    page2.insert_text(
        (72, 100),
        "A model is a quantitative method that applies statistical,\n"
        "economic, financial or mathematical theories.",
        fontsize=11,
    )
    page2.insert_text((72, 160), "3. Expectations", fontsize=14)
    page2.insert_text(
        (72, 190),
        "Institutions must establish a sound model risk management\n"
        "framework that includes governance, validation and monitoring.",
        fontsize=11,
    )

    doc.save(str(OUTPUT))
    doc.close()
    print(f"Created {OUTPUT}")


if __name__ == "__main__":
    main()
