build: compile

compile: clean
	python3 -m build

pex: compile
	pex -r requirements.txt -o git_guardrails.pex -e git_guardrails.command_line:main . --validate-entry-point

deploy: build
	cp git_guardrails.pex /target/destination.pex

.PHONY: clean

clean:
	rm -rf src/**/*.egg-info build dist $${PEX_ROOT}/build/git_guardrails-*.whl
