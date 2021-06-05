Git Guardrails
==============

|CI| |CodeQL| |Lint| |codecov|

``git_guardrails`` is a CLI intended for use in git hooks (currently
just `pre-push`_), to help software engineers catch potential problems
before they cause problematic side effects.

**This is pre-production software, appropriate for early user testing.
It is not yet intended for use in critical development workflows or at
scale.**

Usage
-----

``git_guardrails validate``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This command will attempt to detect a few situations that may change
whether it’s desirable for the user to push updates to an existing
branch

-  If you’ve lost connectivity with your ``origin`` remote, you’ll be
   alerted, and told to check your VPN/network
-  “upstream” commits that you haven’t pulled down locally will be
   detected, and you’ll be given the opportunity to fetch them before
   pushing
-  If you have *far too many* local commits that have not yet been
   pushed to your remote, you’ll be warned and asked to confirm if you
   wish to proceed (threshold: ``40 commits``) and or stopped
   (threshold: ``80 commits``)

CLI options
^^^^^^^^^^^

All of the following options can be set via environment variables (e.g.,
``--foo bar`` could instead be set via ``GIT_GUARDRAILS_FOO=bar``)

::

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

Integration w/ Your Workflow
----------------------------

It is your responsibility to integrate this into your git workflow, with
the understanding that this CLI will exit with ``1`` if it positi

.. _pre-push: https://www.git-scm.com/docs/githooks#_pre_push

.. |CI| image:: https://github.com/mike-north/git_guardrails/actions/workflows/python-package.yml/badge.svg
   :target: https://github.com/mike-north/git_guardrails/actions/workflows/python-package.yml
.. |CodeQL| image:: https://github.com/mike-north/git_guardrails/actions/workflows/codeql.yml/badge.svg
   :target: https://github.com/mike-north/git_guardrails/actions/workflows/codeql.yml
.. |Lint| image:: https://github.com/mike-north/git_guardrails/actions/workflows/flake8.yml/badge.svg
   :target: https://github.com/mike-north/git_guardrails/actions/workflows/flake8.yml
.. |codecov| image:: https://codecov.io/gh/mike-north/git_guardrails/branch/main/graph/badge.svg?token=OURKHEX488
   :target: https://codecov.io/gh/mike-north/git_guardrails