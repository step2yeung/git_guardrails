import asyncio

from git.repo.base import Repo
from git_guardrails.cli.ux import CLIUX
from git_guardrails.validate.options import ValidateOptions


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)


async def do_validate(cli: CLIUX, opts: ValidateOptions):
    repo = Repo(opts.getWorkingDirectory())
    cli.info(f"Beginning validation: {await opts.getCurrentBranchName(repo)}")
