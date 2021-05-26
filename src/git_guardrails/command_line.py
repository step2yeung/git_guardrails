from click import option, group
from colorama import init as initColorama, Style, Fore
from git_guardrails.cli.ux import CLIUX
from git_guardrails.coroutine import coroutine
from git_guardrails.validate import do_validate
from git_guardrails.validate.cli_options import ValidateCLIOptions

initColorama()

CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help'],
    auto_envvar_prefix='GIT_GUARDRAILS'
)

BANNER_HEADLINE = Style.DIM + "|===|===|===|== " + Style.RESET_ALL + Fore.LIGHTCYAN_EX + "Git Guardrails" + Fore.RESET
+ Style.DIM + " ==|===|===|===|" + Style.RESET_ALL


def printBanner():
    print("\n" + BANNER_HEADLINE)


@group(context_settings=CONTEXT_SETTINGS)
@coroutine
async def main():
    printBanner()
    return


@main.command()
@option('--verbose/--no-verbose', type=bool, default=False)
@option('--working-directory', type=str)
@option('--current-branch', type=str)
@coroutine
async def validate(verbose: bool, working_directory: str, current_branch: str):
    """Examine the current Git workspace and perform some sanity-checking"""
    cliOptions = ValidateCLIOptions(verbose, working_directory, current_branch)
    cli = CLIUX()
    await do_validate(cli, cliOptions)
