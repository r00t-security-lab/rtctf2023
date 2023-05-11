import asyncio as ai
import os
import random
from pathlib import Path
from typing import *
from hashlib import md5

from sqlalchemy import Column, Enum, ForeignKey, Index, UniqueConstraint, Table
from sqlalchemy import select, update, delete, insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Query, WriteOnlyMapped, backref, relationship
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.types import Boolean, Integer, String, Text

from .base import Base

# FIXME 虽然原定的是多对多, 但写着写着就变成一对多了捏

# 中间表
user_file = Table(
    "user_file",  # 表名
    Base.metadata,  # 元数据
    Column("user_id", Integer, ForeignKey("user.id")),  # 外键
    Column("file_id", Integer, ForeignKey("file.id"))  # 外键
)


class User(Base):
    """user页面存储类"""
    __tablename__ = "user"
    __mapper_args__ = {"eager_defaults": True}
    id: Mapped[int] = mapped_column(primary_key=True)
    uname: Mapped[str] = mapped_column(String(256), unique=True, index=True)
    passwd: Mapped[str] = mapped_column(String(256), nullable=True)
    # 添加relationship
    files: Mapped[List["uFile"]] = relationship(
        "uFile", secondary=user_file, lazy="selectin", back_populates="users")


class uFile(Base):
    """File存储"""
    __tablename__ = "file"
    __mapper_args__ = {"eager_defaults": True}
    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(String(256))
    fileMD5: Mapped[str] = mapped_column(String(64))
    users: Mapped[List["User"]] = relationship(
        "User", secondary=user_file, lazy="selectin", back_populates="files")

    @property
    def path(self):
        if not hasattr(self, "_path"):
            self._path = Path(
                "upload")/md5(self.users[0].uname.encode('utf-8')).hexdigest()/self.filename
        return self._path
