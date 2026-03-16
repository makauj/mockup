#!/usr/bin/env python3
"""
Collection Model for SQLAlchemy ORM
This module defines the Collection model which represents a collection of records in a database.
It includes fields for ID, Name, Email, Contact, Date, read_only status, and last updated information.
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy import Date, Boolean, TIMESTAMP, ForeignKey, text
from .database import Base
from datetime import datetime


class Collection(Base):
    __tablename__ = 'collections'
    
    record_id = Column(Integer, primary_key=True, index=True)
    ID = Column(Integer, ForeignKey("other_table.id"), nullable=False)
    Name = Column(String)
    Email = Column(String)
    Contact = Column(String)
    Date = Column(Date, nullable=False, default=lambda: datetime.utcnow().date(), server_default=text("CURRENT_DATE"))
    read_only = Column(Boolean, nullable=False, default=False, server_default=text("FALSE"))
    last_updated_by = Column(String)
    last_updated_at = Column(TIMESTAMP,
                             nullable=False,
                             server_default=text("CURRENT_TIMESTAMP"),
                             default=datetime.utcnow,
                             onupdate=datetime.utcnow
                             )
