#!/usr/bin/env python
""" Collection Management Module
This module provides functions to create, retrieve, and update collections
in a database.
It includes functionality to handle read-only collections and track updates.
"""
from sqlalchemy.orm import Session
from .models import Collection
from schemas import CollectionCreate, CollectionUpdate
from datetime import datetime
from fastapi import HTTPException
from typing import Optional

def create_collection(db: Session, data: CollectionCreate, read_only: bool, user: str):
    db_entry = Collection(**data.dict(), read_only=read_only, last_updated_by=user, last_updated_at=datetime.utcnow())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

def get_collections(db: Session, ID: Optional[int] = None, read_only: Optional[bool] = None) -> list[Collection]:
    query = db.query(Collection)
    if ID is not None:
        query = query.filter(Collection.ID == ID)
    if read_only is not None:
        query = query.filter(Collection.read_only == read_only)
    return query.all()

def update_collection(db: Session, record_id: int, changes: dict, current_user: str):
    obj = db.query(Collection).filter(Collection.record_id == record_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    if obj.read_only:
        raise HTTPException(status_code=403, detail="Record is read-only")
    for k, v in changes.items():
        setattr(obj, k, v)
    obj.last_updated_by = current_user
    obj.last_updated_at = datetime.utcnow()
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
