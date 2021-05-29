import subprocess


def git_default_branch(cwd: str):
    process = subprocess.Popen(['git', 'remote', "show", "origin"],
                               cwd=cwd,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    (stdout, _) = process.communicate()
    [relevant_line] = filter(lambda s: "HEAD branch" in s, str(stdout).split('\\n'))
    [_, branch_name] = relevant_line.split(": ")
    return branch_name
