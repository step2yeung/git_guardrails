from git_guardrails.validate.cli_options import ValidateCLIOptions


def test_creation():
    o = ValidateCLIOptions()
    assert o is not None, "Creation of CLI options instance is successful"


def test_retrieval_of_verbosity():
    o1 = ValidateCLIOptions(verbose=True)
    assert o1.verbose == True, ".verbose=True"
    o2 = ValidateCLIOptions(verbose=False)
    assert o2.verbose == False, "verbose=False"
    o3 = ValidateCLIOptions()
    assert o3.verbose == False, "verbose False by default"


def test_retrieval_of_current_branch():
    o1 = ValidateCLIOptions()
    assert o1.current_branch is None, "current_branch is None if not explicitly set"
    o2 = ValidateCLIOptions(current_branch="fizz")
    assert o2.current_branch == "fizz", "current_branch is passed through, if explicitly set"


def test_retrieval_of_cwd():
    o1 = ValidateCLIOptions()
    assert o1.cwd is None, "cwd is None if not explicitly set"
    o2 = ValidateCLIOptions(cwd="fizz")
    assert o2.cwd == "fizz", "cwd is passed through, if explicitly set"


def test_to_str():
    o1 = ValidateCLIOptions()
    assert str(o1) == "ValidateCLIOptions(cwd=None, verbose=False, current_branch=None)"


def test_to_dict():
    o1 = ValidateCLIOptions()
    d = o1.to_dict()
    assert d["cwd"] is None
    assert d["current_branch"] is None
    assert d["verbose"] is False
