"""Tests for the Roman-numeral CLI wrapper.

Added when coverage measurement revealed `cli.py` had no tests: the suite in
`test_roman.py` exercised only the library. These cover every branch of
`main` — success, the two error exits, and the argument-count guard — so the
example's CLI is verified, not just its library.
"""

import pytest
from cli import main


def test_valid_argument_prints_numeral_and_exits_zero(capsys):
    code = main(["1954"])
    assert code == 0
    assert capsys.readouterr().out.strip() == "MCMLIV"


@pytest.mark.parametrize("arg", ["0", "4000"])
def test_out_of_range_reports_error_and_exits_two(arg, capsys):
    code = main([arg])
    assert code == 2
    assert "error:" in capsys.readouterr().err


def test_non_numeric_argument_exits_two(capsys):
    code = main(["abc"])
    assert code == 2
    assert "error:" in capsys.readouterr().err


@pytest.mark.parametrize("argv", [[], ["1", "2"]])
def test_wrong_argument_count_prints_usage_and_exits_two(argv, capsys):
    code = main(argv)
    assert code == 2
    assert "usage:" in capsys.readouterr().err
