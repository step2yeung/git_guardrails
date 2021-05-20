build: clean
	pex -o git_guardrails.pex git_guardrails -e git_guardrails.command_line:main . --validate-entry-point --disable-cache

deploy: build
	cp git_guardrails.pex /target/destination.pex

.PHONY: clean

clean:
	rm -rf *.egg-info build dist $${PEX_ROOT}/build/git_guardrails-*.whl
