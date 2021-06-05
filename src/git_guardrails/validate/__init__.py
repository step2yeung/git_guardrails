from functools import reduce
from typing import List
from git.exc import InvalidGitRepositoryError  # type: ignore
from git.objects.commit import Commit  # type: ignore
from git.refs.head import Head  # type: ignore
from git.refs.remote import RemoteReference  # type: ignore
from git.remote import Remote  # type: ignore
from yaspin import yaspin  # type: ignore

from git.repo.base import Repo  # type: ignore
from git_guardrails.cli.ux import CLIUX
from git_guardrails.cli.value_format import format_branch_name, format_cli_command, format_commit, format_highlight
from git_guardrails.cli.value_format import format_integer, format_remote_name
from git_guardrails.errors import UserBypassException, UserBypassableWarning
from git_guardrails.errors import LikelyUserErrorException, NonApplicableSituationException, UnhandledSituationException
from git_guardrails.git_utils import git_default_branch, git_does_commit_exist_locally, git_ls_remote
from git_guardrails.validate.options import ValidateOptions
from git_guardrails.coroutine import as_async


@as_async
def get_default_git_branch(repo: Repo) -> str:
    with yaspin().white.bold as sp:
        sp.text = "determining default branch"
        default_branch = git_default_branch(repo)
        sp.text = ''
        sp.stop()
        return default_branch


def validate_remotes(repo: Repo):
    remotes = repo.remotes   # remotes
    num_remotes = len(remotes)
    if (num_remotes == 0):
        raise NonApplicableSituationException(
            'No git remotes found',
            "".join(
                [
                    format_cli_command('git_guardrails validate'),
                    " is intended for ",
                    "use when pushing new code to a remote, and no remotes were found."
                ]
            )
        )


def get_branch_information(repo: Repo, branch_name: str) -> Head:
    branch_head: Head = repo.heads[branch_name]
    if (branch_head is None):
        raise UnhandledSituationException(
            f"Could not find branch {branch_name}",
            f"A branch called '{branch_name}' could not be found in repo {repo.working_dir()}"
        )
    return branch_head


def determine_whether_to_auto_fetch(cli: CLIUX, opts: ValidateOptions, active_branch_tracked_ref: RemoteReference):
    user_response = ""
    if opts.is_auto_fetch_enabled() == True:
        cli.debug('User provided --auto-fetch CLI argument. Proceeding as instructed')
        user_response = 'y'
    elif opts.is_auto_fetch_enabled() == False:
        cli.debug('User provided --no-auto-fetch CLI argument. Halting as instructed')
        raise UserBypassException(f"""user decided not to download new commits from {
                active_branch_tracked_ref.name}""")

    while user_response not in ['y', 'Y']:
        user_response = input("Would you like to download these new commits? [y/n]")
        if user_response in ['N', 'n']:
            cli.debug(f"When asked whether we can download new commits, user response was {user_response}")
            raise UserBypassException(f"""user decided not to download new commits from {
                active_branch_tracked_ref.name}""")
        if user_response not in ['y', 'Y']:
            cli.warning(f"Invalid response detected: '{user_response}'. Please answer 'Y' or 'N'.")


def validate_merge_bases_with_default_branch(cli: CLIUX,
                                             repo: Repo,
                                             active_branch_name: str,
                                             default_branch_name: str) -> Commit:
    merge_bases = repo.merge_base(default_branch_name, active_branch_name)
    merge_bases_csv = ", ".join(map(lambda c: c.hexsha[0:8], merge_bases))
    cli.debug(f"merge_bases: {merge_bases_csv}")
    num_merge_bases = len(merge_bases)
    if (num_merge_bases == 0):
        raise UnhandledSituationException(
            'No merge-base commit found',
            f"""No merge-base commits between branches {format_branch_name(default_branch_name) } and {
            format_branch_name(active_branch_name) } could be found, so validation could not be performed.""")
    if (num_merge_bases > 1):
        description = " ".join(
            [
                f"Multiple ({format_integer(num_merge_bases)}) merge-base commits between branches",
                format_branch_name(default_branch_name),
                "and",
                format_branch_name(active_branch_name),
                "were found:"
            ]
        )
        commits_description = reduce(lambda a, b: f"{a}\n- {b}", map(format_commit, merge_bases), "")
        raise UnhandledSituationException(
            'Multiple merge-base commits found',
            description + commits_description)
    return merge_bases[0]


async def validate_branches_and_merge_bases(cli: CLIUX, repo: Repo, opts: ValidateOptions):

    active_branch = get_branch_information(repo, await opts.get_current_branch_name(repo))  # current_branch
    cli.debug(f"active branch: {active_branch.name} @ {active_branch.commit.hexsha}")
    default_branch = get_branch_information(repo, await get_default_git_branch(repo))  # default branch
    cli.debug(f"default branch: {default_branch.name} @ {default_branch.commit.hexsha}")

    if active_branch == default_branch:
        raise NonApplicableSituationException(
            f"You are on the default branch ({default_branch.name})",
            """git_guardrails is intended to catch potential problems when pushing
review branches, and will not take any action when on a git repo's default branch""")

    cli.debug('validating merge base between review branch and default branch')
    validate_merge_bases_with_default_branch(
        cli=cli,
        repo=repo,
        active_branch_name=active_branch,
        default_branch_name=default_branch
    )
    cli.debug('merge base validation complete')
    return (active_branch, default_branch)


def analyze_review_branch_tracking_situation(cli: CLIUX, repo: Repo, active_branch: Head):

    active_branch_tracked_ref = active_branch.tracking_branch()
    if (active_branch_tracked_ref is None):
        raise NonApplicableSituationException(
            f"Branch {active_branch.name} does not track a remote branch",
            "The currently active branch does not track a remote branch yet, perhaps you have not pushed it yet?")

    cli.info(f"""determined that local branch {format_branch_name(active_branch.name)} tracks upstream branch {
            format_branch_name(active_branch_tracked_ref.remote_head)
            } on remote {format_remote_name(active_branch_tracked_ref.remote_name)}""")

    with yaspin().white.bold as sp:
        sp.text = f"searching for new upstream commits on {active_branch_tracked_ref.name}"
        sp.start()
        latest_remote_sha = git_ls_remote(repo=repo,
                                          ref=active_branch_tracked_ref,
                                          ref_types=["heads"])
        latest_local_sha = active_branch_tracked_ref.commit.hexsha
        sp.stop()
        cli.debug(f"latest commit for local ref {active_branch_tracked_ref.name}: {latest_local_sha}")
        cli.debug(f"""latest commit for tracked branch {active_branch_tracked_ref.remote_head
                      } on remote {active_branch_tracked_ref.remote_name}: {latest_remote_sha}""")

        return (latest_remote_sha, active_branch_tracked_ref)


def offer_to_fetch_from_upstream(cli: CLIUX,
                                 repo: Repo,
                                 opts: ValidateOptions,
                                 active_branch: Head,
                                 active_branch_tracked_ref: RemoteReference):
    cli.warning(f"""New commits on {active_branch_tracked_ref
                } were detected, which have not yet been pulled down to {active_branch.name}""")
    determine_whether_to_auto_fetch(cli, opts, active_branch_tracked_ref)
    origin: Remote = repo.remotes['origin']
    refspec = f"{active_branch.name}:{active_branch_tracked_ref.name}"
    cli.info(f"Fetching new commits for branch {active_branch_tracked_ref.name}")
    cli.debug(f"running 'git fetch' from remote '{origin.name}' with refspec '{refspec}'")
    origin.fetch()
    cli.info(f"Fetch from {origin.name} complete")


def get_truncated_log(repo: Repo, commit: Head, tail_sha: str) -> List[Commit]:
    fifty_first_commits = list(repo.iter_commits(commit, max_count=100))
    commits_after_tail: List[Commit] = []
    found_tail = False
    for c in fifty_first_commits:
        if (found_tail == True):
            continue
        if (c.hexsha == tail_sha):
            found_tail = True
            continue
        commits_after_tail.append(c)
    return commits_after_tail


async def do_validate(cli: CLIUX, opts: ValidateOptions):
    try:
        cwd = opts.get_cwd()  # working directory
        repo = Repo(cwd)  # git repo

        validate_remotes(repo=repo)
        (active_branch, default_branch) = await validate_branches_and_merge_bases(cli=cli, repo=repo, opts=opts)
        (latest_remote_sha, active_branch_tracked_ref) = analyze_review_branch_tracking_situation(cli, repo, active_branch)
        has_latest_commits_from_upstream = git_does_commit_exist_locally(repo=repo, sha=latest_remote_sha)

        if (has_latest_commits_from_upstream == False):
            offer_to_fetch_from_upstream(cli=cli, repo=repo, opts=opts, active_branch=active_branch,
                                         active_branch_tracked_ref=active_branch_tracked_ref)
        cli.info(f"Comparing {active_branch.name} against {active_branch_tracked_ref.name}")
        merge_base = validate_merge_bases_with_default_branch(
            cli, repo, repo.active_branch.name, active_branch_tracked_ref.name)
        cli.debug(f"Identified common commit {merge_base.hexsha[0:8]}")
        cli.debug(f"Local sha: {active_branch.commit.hexsha}")
        cli.debug(f"Upstream sha: {active_branch_tracked_ref.commit.hexsha}")
        new_local_commits = get_truncated_log(repo, active_branch.commit, merge_base.hexsha)
        new_upstream_commits = get_truncated_log(repo, active_branch_tracked_ref.commit, merge_base.hexsha)
        cli.debug(f"new local commits: {new_local_commits}")
        cli.debug(f"new upstream commits: {new_upstream_commits}")

        if (len(new_local_commits) > opts.get_commit_count_hard_fail_threshold()):
            raise LikelyUserErrorException(
                "Very large number of review branch commits",
                f"""An very large {len(new_local_commits)} number of commits were detected on review branch {
                    active_branch.name
                    }, which were not found on tracked branch {active_branch_tracked_ref.name
                    }.

{format_highlight("This may be an indication of an improper rebase!")}

This warning is presented whenever more than {format_integer(opts.get_commit_count_hard_fail_threshold())
} new commits that have not yet been pushed are found on a review branch.

Please take a close look at your review branch, and ensure you don't see any duplicate commits that are already on {
default_branch.name}""")
        elif (len(new_local_commits) > opts.get_commit_count_soft_fail_threshold()):
            raise UserBypassableWarning(
                "Large number of review branch commits",
                f"""An unusually large {format_integer(len(new_local_commits))} number of commits were detected on review branch {
                    active_branch.name
                    }, which were not found on tracked branch {active_branch_tracked_ref.name
                    }.

{format_highlight("This may be an indication of an improper rebase!")}

This warning is presented whenever more than {opts.get_commit_count_soft_fail_threshold()
} new commits, that have not yet been pushed, are found on a review branch.

Please take a close look at your review branch, and ensure you don't see any duplicate commits that are already on {
default_branch.name}""")

    except UserBypassException as ex:
        cli.handle_user_bypass_exception(ex)
    except UserBypassableWarning as ex:
        cli.handle_user_bypassable_warning(ex, bypass_response=(
            "continue" if opts.should_auto_bypass_commit_count_soft_fail() else None))
    except NonApplicableSituationException as ex:
        cli.handle_non_applicable_situation_exception(ex)
    except UnhandledSituationException as ex:
        cli.handle_unhandled_situation_exception(ex)
    except InvalidGitRepositoryError:
        cli.error(f"""git_guardrails is only intended for use within a git repository directory
{cwd} does not seem to be a git repository""")
