build: compile

compile: clean
	python3 -m pip install --upgrade pip && python3 -m pip install flake8 pytest && pip install -r requirements.txt
pex:
	pex -r requirements.txt -o git_guardrails.pex -e git_guardrails.command_line:main . --validate-entry-point

deploy: build
	cp git_guardrails.pex /target/destination.pex

test: build
	pytest tests/*

watch-test: build
	ptw tests/*

.PHONY: clean

clean:
	rm -rf src/**/*.egg-info build dist $${PEX_ROOT}/build/git_guardrails-*.whl
