#!/usr/bin/env python3
"""
Collection Management Schemas
This module defines Pydantic models for validating and serializing collection data.
It includes models for creating, updating, and reading collections,
as well as handling read-only collections.
"""
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class CollectionBase(BaseModel):
    ID: int
    Name: Optional[str]
    Email: Optional[str]
    Contact: Optional[str]
    Date: Optional[date]


class CollectionCreate(CollectionBase):
    pass


class CollectionUpdate(BaseModel):
    Name: Optional[str]
    Email: Optional[str]
    Contact: Optional[str]
    Date: Optional[date]
    last_updated_by: str


class CollectionOut(CollectionBase):
    record_id: int
    read_only: bool
    last_updated_by: Optional[str]
    last_updated_at: datetime

    class Config:
        orm_mode = True

class ReadOnlyCollection(CollectionOut):
    read_only: bool = True