import click
from git_guardrails.cli.ux import CLIUX, generate_welcome_banner
from git_guardrails.coroutine import coroutine
from git_guardrails.validate import do_validate
from git_guardrails.validate.cli_options import ValidateCLIOptions
from git_guardrails.validate.options import ValidateOptions
from logging import DEBUG, INFO

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
@click.option('-v', '--verbose/--no-verbose', type=bool, default=False)
@click.option('--cwd', type=str)
@click.option('--current-branch', type=str)
@click.option('--color/--no-color', type=bool, default=True)
@click.option('--tty/--no-tty', type=bool)
@click.option('--auto-fetch/--no-auto-fetch', type=bool, default=False)
@click.option('--auto-rebase/--no-auto-rebase', type=bool, default=False)
@coroutine
async def validate(verbose: bool,
                   cwd: str,
                   current_branch: str,
                   color: bool,
                   tty: bool,
                   auto_fetch: bool,
                   auto_rebase: bool):
    """Examine the current Git workspace and perform some sanity-checking"""
    cliOptions = ValidateCLIOptions(
        verbose=verbose,
        cwd=cwd,
        current_branch=current_branch,
        color=color,
        tty=tty,
        auto_fetch=auto_fetch,
        auto_rebase=auto_rebase
    )
    opts = ValidateOptions(cliOptions)
    log_level = DEBUG if opts.is_verbose() else INFO
    cli = CLIUX(
        log_level=log_level,
        supports_color=opts.is_terminal_color_supported(),
        supports_tty=opts.is_terminal_tty_supported()
    )
    await do_validate(cli, opts)
