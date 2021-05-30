from git.refs.remote import RemoteReference  # type: ignore
from git.repo import Repo  # type: ignore
import subprocess
from typing import List, Literal, Union


def git_default_branch(repo: Repo):
    process = subprocess.Popen(['git', 'remote', "show", "origin"],
                               cwd=repo.working_dir,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    (stdout, _) = process.communicate()
    [relevant_line] = filter(lambda s: "HEAD branch" in s, str(stdout).split('\\n'))
    [_, branch_name] = relevant_line.split(": ")
    return branch_name


def git_ls_remote(repo: Repo, ref: RemoteReference, ref_types: List[Union[Literal["heads", "tags"]]]) -> str:
    command_args = ['git', 'ls-remote']
    if ("heads" in ref_types):
        command_args.append("-h")
    remote_name = ref.remote_name
    remote_branch_name = ref.name.replace(f"{remote_name}/", "")
    command_args.append(remote_name)
    command_args.append(remote_branch_name)

    process = subprocess.Popen(command_args,
                               cwd=repo.working_dir,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    (stdout, _) = process.communicate()
    ls_remote_output = stdout.decode('UTF-8')

    [latest_sha, _] = ls_remote_output.split()
    return latest_sha


def git_does_commit_exist_locally(repo: Repo, sha: str) -> bool:
    try:
        repo.rev_parse(sha)
        return True
    except ValueError:
        return False
