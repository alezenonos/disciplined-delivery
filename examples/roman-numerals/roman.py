"""Convert integers to Roman numerals.

A deliberately tiny library used as a worked example of the
`disciplined-delivery` skill: it was built test-first, one numeral at a time,
with the full suite green before being handed back for review.
"""

# Subtractive pairs (e.g. 900 = "CM") are listed alongside the additive
# numerals and tried high-to-low, so a single greedy pass yields the
# canonical, minimal spelling for any supported value.
_NUMERALS = (
    (1000, "M"),
    (900, "CM"),
    (500, "D"),
    (400, "CD"),
    (100, "C"),
    (90, "XC"),
    (50, "L"),
    (40, "XL"),
    (10, "X"),
    (9, "IX"),
    (5, "V"),
    (4, "IV"),
    (1, "I"),
)

_MIN, _MAX = 1, 3999


def to_roman(number: int) -> str:
    """Return the Roman numeral for ``number``.

    Args:
        number: An integer in the inclusive range 1..3999. Roman numerals have
            no zero or negatives, and 3999 ("MMMCMXCIX") is the largest value
            expressible without overline notation, so the range is bounded.

    Returns:
        The canonical Roman numeral, e.g. ``to_roman(1954) == "MCMLIV"``.

    Raises:
        TypeError: If ``number`` is not an ``int`` (``bool`` is rejected too,
            since ``True``/``False`` are not meaningful numerals).
        ValueError: If ``number`` is outside 1..3999.
    """
    if not isinstance(number, int) or isinstance(number, bool):
        raise TypeError(f"number must be an int, got {type(number).__name__}")
    if not _MIN <= number <= _MAX:
        raise ValueError(f"number must be in {_MIN}..{_MAX}, got {number}")

    parts = []
    for value, symbol in _NUMERALS:
        count, number = divmod(number, value)
        parts.append(symbol * count)
    return "".join(parts)
