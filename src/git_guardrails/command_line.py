import click
from subprocess import Popen
import asyncio
import time
from functools import wraps
from colorama import init as initColorama
from colorama import Fore, Back, Style
from git import Repo
import os

initColorama()

def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)


@click.command()
@coro
async def main():
    """Example script."""
    print(Fore.RED + 'some red text' + Fore.RESET)
    cwd = os.getcwd()
    repo = Repo(cwd)
    assert not repo.bare
    firstRemote = repo.remotes[0]
    print(firstRemote.name)
    print(firstRemote.url)
    print(f"started at {time.strftime('%X')}")
    await say_after(1, 'hello')
    p = Popen(['sleep', '2'])  # something long running
    # ... do other stuff while subprocess is running
    p.wait()
    click.echo('Hello World!')
    print(f"finished at {time.strftime('%X')}")
