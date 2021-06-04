build: compile

setup:
	python3 -m pip install --upgrade pip && pip install -r requirements_dev.txt && pip install -r requirements.txt

compile: clean
	pipenv install
pex:
	pipenv run pex -r requirements.txt -o git_guardrails.pex -e git_guardrails.command_line:main . --validate-entry-point

deploy: build
	cp git_guardrails.pex /target/destination.pex

test: build
	pipenv run pytest

lint: build
	pipenv run flake8
	pipenv run mypy .

watch-test: build
	pipenv run ptw

run-validate: build
	pipenv run git_guardrails validate

.PHONY: clean docs

clean: setup
	pipenv clean && rm -rf src/**/*.egg-info build dist $${PEX_ROOT}/build/git_guardrails-*.whl

# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

docs:
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
