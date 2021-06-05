import click
from git_guardrails.cli.ux import CLIUX, generate_welcome_banner
from git_guardrails.coroutine import coroutine
from git_guardrails.validate import do_validate
from git_guardrails.validate.cli_options import DEFAULT_COMMIT_COUNT_HARD_FAIL_THRESHOLD
from git_guardrails.validate.cli_options import DEFAULT_COMMIT_COUNT_SOFT_FAIL_THRESHOLD
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
@click.option('--commit-count-soft-fail-threshold', type=int, default=DEFAULT_COMMIT_COUNT_HARD_FAIL_THRESHOLD)
@click.option('--commit-count-hard-fail-threshold', type=int, default=DEFAULT_COMMIT_COUNT_SOFT_FAIL_THRESHOLD)
@click.option('--commit-count-auto-bypass-soft-fail', type=bool, default=False, hidden=True)
@coroutine
async def validate(verbose: bool,
                   cwd: str,
                   current_branch: str,
                   color: bool,
                   tty: bool,
                   auto_fetch: bool,
                   commit_count_soft_fail_threshold: bool,
                   commit_count_hard_fail_threshold: bool,
                   commit_count_auto_bypass_soft_fail: bool):
    """Examine the current Git workspace and perform some sanity-checking"""
    cliOptions = ValidateCLIOptions(
        verbose=verbose,
        cwd=cwd,
        current_branch=current_branch,
        color=color,
        tty=tty,
        auto_fetch=auto_fetch,
        commit_count_soft_fail_threshold=commit_count_soft_fail_threshold,
        commit_count_hard_fail_threshold=commit_count_hard_fail_threshold,
        commit_count_auto_bypass_soft_fail=commit_count_auto_bypass_soft_fail
    )
    opts = ValidateOptions(cliOptions)
    log_level = DEBUG if opts.is_verbose() else INFO
    cli = CLIUX(
        log_level=log_level,
        supports_color=opts.is_terminal_color_supported(),
        supports_tty=opts.is_terminal_tty_supported()
    )
    await do_validate(cli, opts)
