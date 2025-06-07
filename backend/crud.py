#!/usr/bin/env python
""" Collection Management Module
This module provides functions to create, retrieve, and update collections
in a database.
It includes functionality to handle read-only collections and track updates.
"""
from sqlalchemy.orm import Session
from models import Collection
from schemas import CollectionCreate, CollectionUpdate
from datetime import datetime

def create_collection(db: Session, data: CollectionCreate, read_only: bool, user: str):
    db_entry = Collection(**data.dict(), read_only=read_only, last_updated_by=user, last_updated_at=datetime.utcnow())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

def get_collections(db: Session, ID: int, read_only: bool) -> list[Collection]:
    query = db.query(Collection)
    if ID:
        query = query.filter(Collection.ID == ID)
    if read_only is not None:
        query = query.filter(Collection.read_only == read_only)
    return query.all()

def update_collection(db: Session, record_id: int, update_data: CollectionUpdate):
    db_obj = db.query(Collection).get(record_id)
    if db_obj.read_only:
        raise ValueError("Row is read-only")
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(db_obj, key, value)
    db_obj.last_updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_obj)
    return db_obj
