import asyncio

from git.repo.base import Repo
from git_guardrails.cli.ux import CLIUX
from git_guardrails.validate.options import ValidateOptions


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)


async def do_validate(cli: CLIUX, opts: ValidateOptions):
    repo = Repo(opts.getWorkingDirectory())
    branch_name = await opts.getCurrentBranchName(repo)
    cli.info(f"Beginning validation: {branch_name}")
