build: compile

compile: clean
	python3 -m pip install --upgrade pip && python3 -m pip install flake8 pytest && pip install -r requirements.txt && pip install -r requirements_dev.txt
pex:
	pex -r requirements.txt -o git_guardrails.pex -e git_guardrails.command_line:main . --validate-entry-point

deploy: build
	cp git_guardrails.pex /target/destination.pex

test: build
	pytest

lint: build
	flake8
	mypy .

watch-test: build
	ptw

.PHONY: clean docs

clean:
	rm -rf src/**/*.egg-info build dist $${PEX_ROOT}/build/git_guardrails-*.whl

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
