#!/usr/bin/env python3
""" Database connection setup for a PostgreSQL database using SQLAlchemy.
This script sets up the database connection parameters and creates a session
factory for use in the application.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL = "postgresql://user:pass@host:port/dbname"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
