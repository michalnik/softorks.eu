.PHONY: help venv install mypy isort lint clean

PYTHON = .venv/bin/python
PIP = .venv/bin/pip

help:
	@echo "Usage:"
	@echo "  make venv        - It'll create virtual environment (.venv), if it has not been created still"
	@echo "  make install     - Project instalation in editable mode with dev dependencies"
	@echo "  make mypy        - It'll run mypy on softorks"
	@echo "  make isort       - It'll run isort on softorks"
	@echo "  make lint        - Run mypy and isort together"
	@echo "  make clean       - Deleting __pycache__ a .mypy_cache"
	@echo "  make run         - Running development server of Django"

venv:
	@if [ -d ".venv" ]; then \
		echo "Virtual environment .venv does exist."; \
	else \
		echo "I am creating virtual environment .venv with python3.13..."; \
		python3.13 -m venv .venv; \
		echo "Virtual environment created in .venv."; \
	fi

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -e ".[dev]"
	@echo "Project installed in editable mode with dev dependencies"

mypy:
	(cd softorks && ../$(PYTHON) -m mypy .)

isort:
	(cd softorks && ../$(PYTHON) -m isort .)

lint: mypy isort

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache
	@echo "Cleaned __pycache__ and .mypy_cache"

migrate: venv
	(cd softorks && ../$(PYTHON) manage.py migrate)

run: migrate
	(cd softorks && ../$(PYTHON) manage.py runserver)
