import asyncio as ai
import os
import random
from typing import *

from sqlalchemy import Column, Enum, ForeignKey, Index, UniqueConstraint
from sqlalchemy import select, update, delete, insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Query, WriteOnlyMapped, backref, relationship
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.types import Boolean, Integer, String, Text, LargeBinary, JSON

from .base import Base


class User(Base):
  __tablename__ = "users"
  __mapper_args__ = {"eager_defaults": True}
  id: Mapped[int] = mapped_column(primary_key=True)
  username: Mapped[str] = mapped_column(String(256))
  password: Mapped[str] = mapped_column(String(256))


class PhishTemplate(Base):
  __tablename__ = "templates"
  __mapper_args__ = {"eager_defaults": True}
  id: Mapped[int] = mapped_column(primary_key=True)
  path: Mapped[str] = mapped_column(String(256), unique=True)
  html: Mapped[str] = mapped_column(Text, default="")

