#!/usr/bin/env python3
"""
Excel parser for collection data.
This script reads an Excel file and extracts collection data into a list
of CollectionCreate objects.
It assumes the Excel file has columns 'ID', 'Name', 'Contact', and 'Date'.
"""
import pandas as pd
from datetime import date, datetime
from typing import Any
from .schemas import CollectionCreate


def _as_optional_string(value: Any) -> str | None:
    if pd.isna(value):
        return None
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def parse_excel(file) -> list[tuple[CollectionCreate, bool]]:
    df = pd.read_excel(file)
    required_columns = {"ID"}
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise ValueError(f"Excel is missing required columns: {', '.join(sorted(missing_columns))}")

    results = []
    for _, row in df.iterrows():
        id_val = row.get("ID")
        name = row.get('Name')
        contact = row.get('Contact')
        date_val = row.get("Date")

        if pd.notna(id_val):
            normalized_name = _as_optional_string(name)
            normalized_contact = _as_optional_string(contact)

            if pd.notna(date_val):
                if isinstance(date_val, datetime):
                    parsed_date = date_val.date()
                elif isinstance(date_val, date):
                    parsed_date = date_val
                else:
                    parsed_date = pd.to_datetime(date_val).date()
            else:
                parsed_date = datetime.today().date()

            # A row is read-only only when ID, Name, and Contact are all present.
            read_only = normalized_name is not None and normalized_contact is not None
            entry = CollectionCreate(
                ID=int(id_val),
                Name=normalized_name,
                Email=None,
                Contact=normalized_contact,
                Date=parsed_date,
            )
            results.append((entry, read_only))
    return results