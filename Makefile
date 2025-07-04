.PHONY: install update get-test-data test test-linting test-pycodestyle test-bandit test-pytest test-notebooks test-coverage show-outdated docs publish

all:

install:
	pip install poetry
	poetry install
	${MAKE} get-test-data

update upgrade:
	pip install --upgrade poetry
	poetry update

get-test-data:
	mkdir -p tests/test_data
	cd tests/test_data && rm -rf *
	cd tests/test_data && wget -O test_data.tar.gz https://aurora.phys.ucalgary.ca/public/github_tests/pyucrio_test_data.tar.gz
	cd tests/test_data && tar -zxvf test_data.tar.gz && rm test_data.tar.gz

docs:
	poetry run pdoc3 --html --force --output-dir docs/generated pyucrio --config "lunr_search={'fuzziness': 1}" --template-dir docs/templates

test: test-linting

test-linting: test-ruff test-pycodestyle test-pyright test-bandit

test-ruff:
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

test-pyright:
	@printf "Running pyright tests\n+++++++++++++++++++++++++++\n"
	pyright
	@printf "\n\n"

test-bandit:
	@printf "Running bandit tests\n+++++++++++++++++++++++++++\n"
	bandit -c pyproject.toml -r -ii pyucrio
	@printf "\n\n"

test-pytest:
	pytest -n 4 --cov=pyucrio --cov-report=

test-notebooks:
	pytest -n 4 --nbmake examples/notebooks --ignore-glob=examples/notebooks/**/in_development/*.ipynb

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
