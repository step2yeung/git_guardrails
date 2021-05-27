import click
from git_guardrails.cli.ux import CLIUX, generate_welcome_banner
from git_guardrails.coroutine import coroutine
from git_guardrails.validate import do_validate
from git_guardrails.validate.cli_options import ValidateCLIOptions

CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help'],
    auto_envvar_prefix='GIT_GUARDRAILS'
)


@click.group(context_settings=CONTEXT_SETTINGS)
@coroutine
async def main():
    print(generate_welcome_banner())
    return


@main.command()
@click.option('--verbose/--no-verbose', type=bool, default=False)
@click.option('--working-directory', type=str)
@click.option('--current-branch', type=str)
@click.option('--color/--no-color', type=bool, default=True)
@click.option('--tty/--no-tty', type=bool)
@coroutine
async def validate(verbose: bool,
                   working_directory: str,
                   current_branch: str,
                   color: bool,
                   tty: bool):
    """Examine the current Git workspace and perform some sanity-checking"""
    cliOptions = ValidateCLIOptions(verbose=verbose, working_directory=working_directory,
                                    current_branch=current_branch, color=color, tty=tty)
    cli = CLIUX()
    await do_validate(cli, cliOptions)
