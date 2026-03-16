#!/usr/bin/env python3
"""
Collection Management Schemas
This module defines Pydantic models for validating and serializing collection data.
It includes models for creating, updating, and reading collections,
as well as handling read-only collections.
"""
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date, datetime


class CollectionBase(BaseModel):
    ID: int
    Name: Optional[str] = None
    Email: Optional[str] = None
    Contact: Optional[str] = None
    Date: Optional[date] = None


class CollectionCreate(CollectionBase):
    pass


class CollectionUpdate(BaseModel):
    Name: Optional[str] = None
    Email: Optional[str] = None
    Contact: Optional[str] = None
    Date: Optional[date] = None


class CollectionOut(CollectionBase):
    record_id: int
    read_only: bool
    last_updated_by: Optional[str]
    last_updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ReadOnlyCollection(CollectionOut):
    read_only: bool = True


class Token(BaseModel):
    access_token: str
    token_type: str