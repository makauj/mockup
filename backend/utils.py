#!/usr/bin/env python3
"""
Excel parser for collection data.
This script reads an Excel file and extracts collection data into a list
of CollectionCreate objects.
It assumes the Excel file has columns 'ID', 'Name', 'Contact', and 'Date'.
"""
import pandas as pd
from datetime import datetime
from .schemas import CollectionCreate


def parse_excel(file) -> list[CollectionCreate]:
    df = pd.read_excel(file)
    results = []
    for _, row in df.iterrows():
        id_val = row['ID']
        name = row.get('Name')
        contact = row.get('Contact')
        date = row.get('Date') if pd.notna(row.get('Date')) else datetime.today().date()

        if pd.notna(id_val):
            filled = sum(pd.notna([id_val, name, contact]))
            read_only = filled >= 3
            entry = CollectionCreate(
                ID=int(id_val),
                Name=name if pd.notna(name) else None,
                Contact=contact if pd.notna(contact) else None,
                Date=date
            )
            results.append((entry, read_only))
    return results