from click import option, group
from colorama import init as initColorama
from git_guardrails.cli.ux import CLIUX
from git_guardrails.coroutine import coroutine
from git_guardrails.validate import validate_entry
from git_guardrails.validate.cli_options import ValidateCLIOptions
from git_guardrails.validate.options import ValidateOptions

initColorama()

CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help'],
    auto_envvar_prefix='GIT_GUARDRAILS'
)


@group(context_settings=CONTEXT_SETTINGS)
@coroutine
async def main():
    return


@main.command()
@option('--verbose/--no-verbose', type=bool, default=False)
@option('--current-branch', type=str)
@coroutine
async def validate(verbose: bool, current_branch: str):
    """Examine the current Git workspace and perform some sanity-checking"""

    cliOptions = ValidateCLIOptions(verbose, current_branch)
    cli = CLIUX()
    await validate_entry(cli, ValidateOptions(cliOptions))
