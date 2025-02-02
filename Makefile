.PHONY: install update test test-linting test-pycodestyle test-bandit test-pytest test-pytest-search test-coverage show-outdated docs publish

all:

poetry:
	python -m pip install poetry

install: poetry
	poetry install

update upgrade:
	python -m pip install --upgrade poetry
	poetry update

docs:
	poetry run pdoc3 --html --force --output-dir docs/generated pyucrio --config "lunr_search={'fuzziness': 1}" --template-dir docs/templates

test: test-linting

test-linting: test-ruff test-pycodestyle test-pyright test-bandit

test-ruff ruff:
	@printf "Running ruff tests\n+++++++++++++++++++++++++++\n"
	ruff check --respect-gitignore --quiet pyucrio
	ruff check --respect-gitignore --quiet tests
	ruff check --respect-gitignore --quiet tools
	@printf "\n\n"

test-pycodestyle:
	@printf "Running pycodestyle tests\n+++++++++++++++++++++++++++\n"
	pycodestyle --config=.pycodestyle pyucrio
	pycodestyle --config=.pycodestyle tests
	pycodestyle --config=.pycodestyle tools
	@printf "\n\n"

test-pyright pyright:
	@printf "Running pyright tests\n+++++++++++++++++++++++++++\n"
	pyright
	@printf "\n\n"

test-bandit bandit:
	@printf "Running bandit tests\n+++++++++++++++++++++++++++\n"
	bandit -c pyproject.toml -r -ii pyucrio
	@printf "\n\n"

test-pytest pytest:
	pytest -n 2 --cov=pyucrio --cov-report= --maxfail=1

test-coverage coverage:
	coverage report
	@tools/update_coverage_file.py

show-outdated:
	poetry show --outdated

tool-checks:
	@./tools/check_for_license.py
	@./tools/check_docstrings.py

publish:
	${MAKE} test
	${MAKE} tool-checks
	poetry build
	poetry publish
	@rm -rf pyucrio.egg-info build dist
