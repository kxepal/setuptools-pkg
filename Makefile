# Copyright (C) 2016 Alexander Shorin
# All rights reserved.
#
# This software is licensed as described in the file LICENSE, which
# you should have received as part of this distribution.
#


AUTOFLAKE       := autoflake
COVERAGE        := coverage
FLAKE8          := flake8
GIT             := git
ISORT           := isort
PIP             := pip
PYLINT          := pylint
PYTEST          := py.test
PROJECT         := setuptools_pkg
PYTHON          := python
VIRTUALENV      := virtualenv
VENV_PATH       := venv


.PHONY: all
all: help


.PHONY: check
# target: check - Runs tests
check:
	@$(PYTEST) -v -l tests


.PHONY: check-all
# target: check-all - Runs lint checks, tests and generates coverage report
check-all: check-lint check-coverage


.PHONY: check-coverage
# target: check-coverage - Runs tests and generates coverage report
check-coverage:
	@$(PYTEST) --cov=src --cov=tests --cov-report=term-missing --cov-report=html tests/


.PHONY: check-lint
# target: check-lint - Runs lint checks
check-lint: check-imports check-codestyle check-errors

check-imports:
	@$(ISORT) -df -c -rc setup.py src/ tests/
check-codestyle:
	@$(FLAKE8) --statistics --show-pep8 --show-source setup.py src/ tests/
check-errors:
	@$(PYLINT) --rcfile=.pylint.rc -E src/$(PROJECT) tests/


.PHONY: clean
# target: clean - Removes intermediate and generated files
clean:
	@find {src,tests} -type f -name '*.py[co]' -delete
	@find {src,tests} -type d -name '__pycache__' -delete
	@rm -f .coverage
	@rm -rf {build,htmlcov,cover,coverage}
	@rm -rf "$(PROJECT).egg-info"
	@$(PYTHON) setup.py clean


.PHONY: develop
# target: develop - Installs package in develop mode
develop:
	@$(PIP) install --upgrade setuptools
	@$(PIP) install -e .[develop]


.PHONY: format
# target: format - Tries to format the code according the coding styles
format: format-imports format-codestyle

format-imports:
	@$(ISORT) -rc setup.py src/ tests/
format-codestyle:
	@$(AUTOFLAKE) -i -r --remove-all-unused-imports --remove-unused-variables setup.py src/ tests/


.PHONY: help
# target: help - Prints this help
help:
	@egrep "^# target: " Makefile \
		| sed -e 's/^# target: //g' \
		| sort -sh \
		| awk '{printf("    %-15s", $$1); $$1=$$2=""; print "-" $$0}'


.PHONY: purge
# target: purge - Removes all unversioned files and resets repository
purge:
	@$(GIT) reset --hard HEAD
	@$(GIT) clean -xdff


.PHONY: venv
# target: venv - Creates virtual environment
venv:
	@$(VIRTUALENV) -p $(PYTHON) $(VENV_PATH)


.PHONY: version
# target: version - Generates project release version
version:
	@$(GIT) describe --always --tags \
		| sed -r 's/^(.*)-(.*)-(.*)/\1.\2+\3/' \
		> VERSION
