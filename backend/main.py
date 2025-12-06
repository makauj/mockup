#!/usr/bin/env python
"""FastAPI application for managing collections with Excel import functionality.
This application allows users to upload an Excel file containing collection
data, which is then parsed and stored in a database.
It also provides endpoints to read and update collections."""
from fastapi import FastAPI, Depends, UploadFile, File, HTTPException, Header
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
import .models, .crud, .schemas # type: ignore
from .utils import parse_excel

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(x_user: str | None = Header(None)):
    # simple header-based current user; replace with proper auth as needed
    return x_user or "import_user"

@app.post("/upload/")
async def upload_excel(file: UploadFile = File(...), db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    entries = parse_excel(file.file)
    results = []
    for entry, read_only in entries:
        result = crud.create_collection(db, entry, read_only, user=user)
        results.append(result)
    return results

@app.get("/collections/", response_model=list[schemas.CollectionOut])
def read_collections(ID: int = None, read_only: bool = None, db: Session = Depends(get_db)):
    return crud.get_collections(db, ID=ID, read_only=read_only)

@app.put("/collections/{record_id}", response_model=schemas.CollectionOut)
def update_collection(record_id: int, data: schemas.CollectionUpdate, db: Session = Depends(get_db)):
    try:
        return crud.update_collection(db, record_id, data)
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))