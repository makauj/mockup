#!/usr/bin/env python
"""FastAPI application for managing collections with Excel import functionality.
This application allows users to upload an Excel file containing collection
data, which is then parsed and stored in a database.
It also provides endpoints to read and update collections."""
from fastapi import FastAPI, Depends, UploadFile, File, HTTPException, Query
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional
from .database import SessionLocal
from . import models, crud, schemas
from .auth import get_current_user, authenticate_form_user, create_access_token
from .utils import parse_excel

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/auth/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    username = authenticate_form_user(form_data.username, form_data.password)
    if not username:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(username)
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/upload/", response_model=list[schemas.CollectionOut], status_code=201)
async def upload_excel(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user),
):
    filename = (file.filename or "").lower()
    if not filename.endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Only .xlsx and .xls files are supported")

    try:
        entries = parse_excel(file.file)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Failed to parse Excel file") from exc

    results = []
    for entry, read_only in entries:
        result = crud.create_collection(db, entry, read_only, user=user)
        results.append(result)
    return results

@app.get("/collections/", response_model=list[schemas.CollectionOut])
def read_collections(
    ID: Optional[int] = None,
    read_only: Optional[bool] = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    return crud.get_collections(db, ID=ID, read_only=read_only, skip=skip, limit=limit)

@app.put("/collections/{record_id}", response_model=schemas.CollectionOut)
def update_collection(
    record_id: int,
    data: schemas.CollectionUpdate,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user),
):
    return crud.update_collection(db, record_id, data, user)