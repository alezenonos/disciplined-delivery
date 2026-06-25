"""Tests for the Roman numeral converter.

Written test-first to demonstrate the disciplined-delivery loop: each case
below was red before the matching line of `roman.to_roman` made it green.
"""

import pytest
from roman import to_roman


@pytest.mark.parametrize(
    ("number", "expected"),
    [
        (1, "I"),
        (2, "II"),
        (3, "III"),
        (4, "IV"),
        (5, "V"),
        (9, "IX"),
        (14, "XIV"),
        (40, "XL"),
        (90, "XC"),
        (400, "CD"),
        (900, "CM"),
        (1954, "MCMLIV"),
        (1990, "MCMXC"),
        (2024, "MMXXIV"),
        (3999, "MMMCMXCIX"),
    ],
)
def test_to_roman_converts_known_values(number, expected):
    assert to_roman(number) == expected


@pytest.mark.parametrize("number", [0, -1, 4000, 10000])
def test_to_roman_rejects_out_of_range(number):
    with pytest.raises(ValueError):
        to_roman(number)


@pytest.mark.parametrize("number", [1.5, "5", None, True])
def test_to_roman_rejects_non_int(number):
    with pytest.raises(TypeError):
        to_roman(number)
