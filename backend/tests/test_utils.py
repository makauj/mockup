from io import BytesIO
from datetime import date

import pandas as pd
import pytest

from backend.utils import parse_excel


def _to_excel_file(df: pd.DataFrame) -> BytesIO:
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    buffer.seek(0)
    return buffer


def test_parse_excel_applies_read_only_and_date_fallback() -> None:
    df = pd.DataFrame(
        [
            {"ID": 1, "Name": "Alice", "Contact": "123", "Date": pd.NaT, "collected": "x"},
            {"ID": 2, "Name": None, "Contact": None, "Date": pd.Timestamp("2026-03-01")},
        ]
    )

    results = parse_excel(_to_excel_file(df))

    assert len(results) == 2

    first_entry, first_read_only = results[0]
    assert first_entry.ID == 1
    assert first_entry.Name == "Alice"
    assert first_entry.Email is None
    assert first_read_only is True
    assert isinstance(first_entry.Date, date)

    second_entry, second_read_only = results[1]
    assert second_entry.ID == 2
    assert second_entry.Name is None
    assert second_entry.Contact is None
    assert second_read_only is False
    assert second_entry.Date == date(2026, 3, 1)


def test_parse_excel_requires_id_column() -> None:
    df = pd.DataFrame([{"Name": "Alice", "Contact": "123"}])

    with pytest.raises(ValueError, match="ID"):
        parse_excel(_to_excel_file(df))
