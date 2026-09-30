.PHONY: setup test lint eval eval-smoke run

setup:
	uv sync --all-extras
	docker compose up -d --wait

test:
	uv run pytest -m "not llm"

lint:
	uv run ruff check src tests
	uv run ruff format --check src tests
	uv run mypy

eval:
	uv run pytest evals/ -m "not llm" --tb=short

eval-smoke:
	uv run pytest evals/ -m "not llm" -k smoke --tb=short

run:
	uv run uvicorn regulens.api:app --reload --port 8000
