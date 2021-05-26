import pytest
from git_guardrails.validate.cli_options import ValidateCLIOptions


def test_creation():
    o = ValidateCLIOptions(True, None, None)
    assert o is not None, "Creation of CLI options instance is successful"


def test_failed_creation():
    with pytest.raises(AssertionError) as excinfo:
        ValidateCLIOptions(None, None, None)
    assert "ValidateCLIOptions#verbose must be either True or False" in str(
        excinfo.value)


def test_retrieval_of_verbosity():
    o1 = ValidateCLIOptions(True, None, None)
    assert o1.verbose == True, ".verbose property is exposed if set to True"
    o2 = ValidateCLIOptions(False, None, None)
    assert o2.verbose == False, ".verbose property is exposed if set to False"
