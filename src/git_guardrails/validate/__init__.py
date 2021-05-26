import json
from git import Repo
from time import strftime
import asyncio
from git_guardrails.cli.ux import CLIUX
from git_guardrails.validate.cli_options import ValidateCLIOptions
from git_guardrails.validate.options import ValidateOptions


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)


async def do_validate(cli: CLIUX, cliOpts: ValidateCLIOptions):
    opts = ValidateOptions(cliOpts)
    repo = Repo(opts.getWorkingDirectory())
    assert not repo.bare
    print(json.dumps(await opts.to_dict(repo)))
    await say_after(1, 'hello')
    print(f"finished at {strftime('%X')}")
    return
