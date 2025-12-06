#!/usr/bin/env python3

# Package exports and metadata for the backend package.
from .main import app
from .schemas import CollectionCreate, CollectionUpdate, CollectionOut, CollectionReadOnly
from .models import Collection
from .crud import create_collection, get_collections, update_collection
from .database import SessionLocal, engine
from .utils import parse_excel

__all__ = [
    "app",
    "CollectionCreate",
    "CollectionUpdate",
    "CollectionOut",
    "CollectionReadOnly",
    "Collection",
    "create_collection",
    "get_collections",
    "update_collection",
    "SessionLocal",
    "engine",
    "parse_excel",
]

__version__ = "0.1.0"
__author__ = "John Makau"
__email__ = "makauwanyoike@gmail.com"
__license__ = "MIT"
__description__ = "A FastAPI application for managing collections with Excel import functionality."
__status__ = "Development"
__copyright__ = "Copyright (c) 2023 John Makau"
