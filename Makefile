build: compile

compile: clean
	python3 -m pip install --upgrade pip && python3 -m pip install flake8 pytest && pip install -r requirements.txt
pex:
	pex -r requirements.txt -o git_guardrails.pex -e git_guardrails.command_line:main . --validate-entry-point

deploy: build
	cp git_guardrails.pex /target/destination.pex

test: build
	pytest

lint: build
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics && \
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

watch-test: build
	ptw

.PHONY: clean

clean:
	rm -rf src/**/*.egg-info build dist $${PEX_ROOT}/build/git_guardrails-*.whl
