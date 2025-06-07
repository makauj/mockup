#!/usr/bin/env python3

import main
import schemas
import models
import crud
import database
__all__ = [
    "main",
    "schemas",
    "models",
    "crud",
    "database"
]
from .main import app
from .schemas import CollectionCreate, CollectionUpdate, CollectionOut, CollectionReadOnly
from .models import Collection
from .crud import create_collection, get_collections, update_collection
from .database import SessionLocal, engine
from .utils import parse_excel
__version__ = "0.1.0"
__author__ = "John Makau"
__email__ = "makauwanyoike@gmail.com"
__license__ = "MIT"
__description__ = "A FastAPI application for managing collections with Excel import functionality."
__url__ = ""
__status__ = "Development"
__all__ += [
    "parse_excel",
    "SessionLocal",
    "engine",
    "CollectionCreate",
    "CollectionUpdate",
    "CollectionOut",
    "CollectionReadOnly",
    "Collection"
]
__version_info__ = tuple(map(int, __version__.split(".")))
__author_info__ = {
    "name": __author__,
    "email": __email__
}
__license_info__ = {
    "name": __license__,
    "url": "https://opensource.org/license/mit/"
}
__description_info__ = {
    "short": __description__,
    "long": "This application allows users to upload an Excel file containing collection data, which is then parsed and stored in a database. It also provides endpoints to read and update collections."
}
__url_info__ = {
    "homepage": __url__,
    "repository": __url__,
    "documentation": __url__
}
__status_info__ = {
    "development": __status__,
    "testing": "Not started",
    "production": "Not started"
}
__copyright__ = "Copyright (c) 2023 John Makau"
