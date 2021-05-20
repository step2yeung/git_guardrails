import click
from subprocess import Popen
import asyncio
import time
from functools import wraps


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
    print(f"started at {time.strftime('%X')}")
    await say_after(1, 'hello')
    p = Popen(['sleep', '2'])  # something long running
    # ... do other stuff while subprocess is running
    p.wait()
    click.echo('Hello World!')
    print(f"finished at {time.strftime('%X')}")
