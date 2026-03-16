#!/usr/bin/env python
""" Collection Management Module
This module provides functions to create, retrieve, and update collections
in a database.
It includes functionality to handle read-only collections and track updates.
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from .models import Collection
from .schemas import CollectionCreate, CollectionUpdate
from datetime import datetime
from fastapi import HTTPException
from typing import Optional
import logging


logger = logging.getLogger(__name__)


def _model_dump(model_obj, *, exclude_unset: bool = False) -> dict:
    if hasattr(model_obj, "model_dump"):
        return model_obj.model_dump(exclude_unset=exclude_unset)
    return model_obj.dict(exclude_unset=exclude_unset)

def create_collection(db: Session, data: CollectionCreate, read_only: bool, user: str):
    db_entry = Collection(
        **_model_dump(data),
        read_only=read_only,
        last_updated_by=user,
        last_updated_at=datetime.utcnow(),
    )
    db.add(db_entry)
    try:
        db.commit()
        db.refresh(db_entry)
        return db_entry
    except IntegrityError as exc:
        db.rollback()
        logger.exception("Integrity error creating collection entry")
        raise HTTPException(status_code=400, detail="Invalid collection data") from exc
    except SQLAlchemyError as exc:
        db.rollback()
        logger.exception("Database error creating collection entry")
        raise HTTPException(status_code=500, detail="Database error while creating collection") from exc

def get_collections(
    db: Session,
    ID: Optional[int] = None,
    read_only: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
) -> list[Collection]:
    query = db.query(Collection)
    if ID is not None:
        query = query.filter(Collection.ID == ID)
    if read_only is not None:
        query = query.filter(Collection.read_only == read_only)
    return query.offset(skip).limit(limit).all()

def update_collection(db: Session, record_id: int, changes: CollectionUpdate, current_user: str):
    obj = db.query(Collection).filter(Collection.record_id == record_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    if bool(getattr(obj, "read_only", False)):
        raise HTTPException(status_code=403, detail="Record is read-only")

    allowed_fields = {"Name", "Email", "Contact", "Date"}
    raw_changes = _model_dump(changes, exclude_unset=True)
    for k, v in raw_changes.items():
        if k in allowed_fields:
            setattr(obj, k, v)

    setattr(obj, "last_updated_by", current_user)
    setattr(obj, "last_updated_at", datetime.utcnow())
    db.add(obj)
    try:
        db.commit()
        db.refresh(obj)
        return obj
    except IntegrityError as exc:
        db.rollback()
        logger.exception("Integrity error updating collection record_id=%s", record_id)
        raise HTTPException(status_code=400, detail="Invalid update payload") from exc
    except SQLAlchemyError as exc:
        db.rollback()
        logger.exception("Database error updating collection record_id=%s", record_id)
        raise HTTPException(status_code=500, detail="Database error while updating collection") from exc
