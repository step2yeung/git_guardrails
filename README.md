# Git Guardrails

[![CI](https://github.com/mike-north/git_guardrails/actions/workflows/python-package.yml/badge.svg)](https://github.com/mike-north/git_guardrails/actions/workflows/python-package.yml)
[![CodeQL](https://github.com/mike-north/git_guardrails/actions/workflows/codeql.yml/badge.svg)](https://github.com/mike-north/git_guardrails/actions/workflows/codeql.yml)
[![Lint](https://github.com/mike-north/git_guardrails/actions/workflows/flake8.yml/badge.svg)](https://github.com/mike-north/git_guardrails/actions/workflows/flake8.yml)
[![codecov](https://codecov.io/gh/mike-north/git_guardrails/branch/main/graph/badge.svg?token=OURKHEX488)](https://codecov.io/gh/mike-north/git_guardrails)

`git_guardrails` is a CLI intended for use in git hooks (currently just [pre-push](https://www.git-scm.com/docs/githooks#_pre_push)), to help
software engineers catch potential problems before they cause problematic side effects.



**This is pre-production software, appropriate for early user testing. It is not yet intended for use in critical development workflows or at scale.**

## Limitations

- This tool assumes that all pull requests target a "default branch" (e.g., `main` or `master`), it may not behave as expected when creating "chain PRs"
- It is assumed that all PRs are performed on the git remote called `origin`
- If both `main` and `master` branches are found on your `origin` git remote, the tool will fail to determine where your PRs are likely to target, and fail (see: #31)
- If you're targeting a branch that doesn't exist anymore (e.g., it's been deleted) the tool will fail (see: #32)

## Usage

### `git_guardrails validate`
This command will attempt to detect a few situations that may change whether it's desirable for the user to push updates to an existing branch

* If you've lost connectivity with your `origin` remote, you'll be alerted, and told to check your VPN/network
* "upstream" commits that you haven't pulled down locally will be detected, and you'll be given the opportunity to fetch them before pushing
* If you have _far too many_ local commits that have not yet been pushed to your remote, you'll be warned and asked to confirm if you wish to proceed (threshold: `40 commits`) and or stopped (threshold: `80 commits`)


#### CLI options
All of the following options can be set via environment variables (e.g., `--foo bar` could instead be set via `GIT_GUARDRAILS_FOO=bar`)


```
Usage: git_guardrails validate [OPTIONS]

  Examine the current Git workspace and perform some sanity-checking

Options:
  -v, --verbose / --no-verbose    extra logging
  --cwd TEXT                      directory to examine (the git repo)
  --current-branch TEXT           name of branch to treat as 'the PR'
  --color / --no-color            terminal color support
  --tty / --no-tty                terminal TTY support
  --auto-fetch / --no-auto-fetch  automatically fetch new upstream commits
  --commit-count-soft-fail-threshold INTEGER
                                  # of new local branch commits before the
                                  user is warned  [default: 80]
  --commit-count-hard-fail-threshold INTEGER
                                  # of new local branch commits before the
                                  user is stopped  [default: 40]
  -h, --help                      Show this message and exit.
```

## Integration w/ Your Workflow
It is your responsibility to integrate this into your git workflow, with the understanding that
this CLI will exit with `1` if it positively identifies a likely problem, and `0` otherwise.

[This](https://githooks.com/) is a great guide to working with Git hooks in general, and tells you everything you need to know in order to get started.

**If you are evaluating or experimenting with this tool, we recommend that you invoke it explicitly directly to see how it responds in various situations**

## Contributing

### Dev environment requirements

**Python 3.7 is required**
```sh
python3 --version
> Python 3.7.10
```

### Setup procedure

Clone this git repo
```sh
git clone git@github.com:mike-north/git_guardrails
cd git_guardrails
```
Install dependencies and build the project
```sh
make
```
Install the local module on your machine
```sh
pip install -e git_guardrails
```

Now go to your home folder and try running
```sh
git_guardrails -h
```

You should see something like the following, if everything is working properly
```
Usage: git_guardrails [OPTIONS] COMMAND [ARGS]...

Options:
  -h, --help  Show this message and exit.

Commands:
  validate  Examine the current Git workspace and perform some...
```

Now you should be able to use `git_guardrails validate` across your local machine, in any git repo


## Legal
Code is covered by the [BSD-2-Clause license](./LICENSE). &copy; 2021 LinkedIn, All Rights Reserved
