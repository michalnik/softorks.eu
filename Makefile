.PHONY: help venv install mypy isort lint clean

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
	@if [ -e ".python-version" ]; then \
		echo "Virtual environment does exist."; \
		cat .python-version; \
	else \
		echo "I am creating virtual environment..."; \
		pyenv virtualenv 3.13.5 softarna-3.13; \
		echo "Virtual environment created."; \
		pyenv local softarna-3.13; \
		cat .python-version; \
	fi

install: venv
	python -m pip install --upgrade pip
	python -m pip install -e ".[dev]"
	@echo "Project installed in editable mode with dev dependencies"

mypy:
	(cd softorks && python -m mypy .)

isort:
	(cd softorks && python -m isort .)

lint: mypy isort

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache
	@echo "Cleaned __pycache__ and .mypy_cache"

migrate: venv
	(cd softorks && python manage.py migrate)

run: migrate
	(cd softorks && python manage.py runserver)
