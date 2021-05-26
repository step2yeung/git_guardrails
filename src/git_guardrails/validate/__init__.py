import json
import click
from colorama import Fore, Back, Style
from git import Repo
from os import getcwd
from subprocess import Popen
from time import strftime
import asyncio
from git_guardrails.cli.ux import CLIUX
from git_guardrails.validate.options import ValidateOptions


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)


async def validate_entry(cli: CLIUX, opts: ValidateOptions):

    print(json.dumps(await opts.to_dict()))
    print(Fore.RED + 'some red text' + Fore.RESET)
    cwd = getcwd()
    repo = Repo(cwd)
    assert not repo.bare
    firstRemote = repo.remotes[0]
    print(firstRemote.name)
    print(firstRemote.url)
    print(f"started at {strftime('%X')}")
    await say_after(1, 'hello')
    p = Popen(['sleep', '2'])  # something long running
    # ... do other stuff while subprocess is running
    p.wait()
    click.echo('Hello World!')
    print(f"finished at {strftime('%X')}")
    return
