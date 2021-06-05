from git_guardrails_test_helpers.git_test_utils import temp_repo_clone, reflog_to_str, temp_repo, create_git_history
from git_guardrails_test_helpers.git_test_utils import commit_all_modified_tracked_files


def test_create_git_history():
    with temp_repo() as repo:
        commit_all_modified_tracked_files(repo, "initial commit")
        create_git_history(repo, [
            (('hello1.txt', 'hello world!'), 'second commit'),
            (('hello2.txt', 'hello world!'), 'third commit'),
            (('hello3.txt', 'hello world!'), 'fourth commit'),
            (('hello4.txt', 'hello world!'), 'fifth commit'),
        ])
        log = repo.head.log()
        assert reflog_to_str(log) == """commit: Switching to master
second commit
third commit
fourth commit
fifth commit"""


def test_create_temp_clone():
    with temp_repo() as upstream:
        commit_all_modified_tracked_files(upstream, "initial commit")
        assert upstream.is_dirty() == False, 'before create_git_history, repo is "clean"'
        create_git_history(upstream, [
            (('hello1.txt', 'hello world!'), 'second commit'),
            (('hello2.txt', 'hello world!'), 'third commit'),
            (('hello3.txt', 'hello world!'), 'fourth commit'),
            (('hello4.txt', 'hello world!'), 'fifth commit'),
        ])
        assert upstream.is_dirty() == False, 'after create_git_history, repo is left "clean"'
        upstream_feature_branch = upstream.create_head('feature-456')
        upstream_feature_branch.checkout()
        assert upstream.active_branch.name == 'feature-456'
        assert upstream.is_dirty() == False, f"{upstream.index.diff(other=upstream_feature_branch.commit)}"
        create_git_history(upstream, [
            (('hello5.txt', 'hello world!'), 'feature commit')
        ])
        assert upstream.is_dirty() == False
        upstream.heads['master'].checkout()
        with temp_repo_clone(upstream, ['feature-456']) as downstream:
            assert downstream.bare == False
            assert list(sorted(map(lambda h: h.name, downstream.heads))) == sorted(['master', 'feature-456'])
