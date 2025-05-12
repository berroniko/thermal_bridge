from datetime import datetime

import pytest

from src.utils import parse_date


@pytest.mark.parametrize("date_string, expected",
                         [('30.12.2024', datetime(2024, 12, 30)),
                          ('3/12/2023', datetime(2023, 12, 3))])
def test_parse_date(date_string, expected):
    assert parse_date(date_str=date_string) == expected
