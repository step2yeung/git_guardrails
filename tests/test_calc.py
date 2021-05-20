from git_guardrails import calculator


def test_answer():
    assert calculator.add(3, 4) == 7
