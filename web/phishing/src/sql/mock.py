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

HTTP_METHODS = {
  "GET": 1,
  "POST": 2,
  "PUT": 4,
  "DELETE": 8,
  "PATCH": 16,
  "OPTIONS": 32,
  "HEAD": 64,
}

class MockInfo(Base):
  """mock页面存储类"""
  __tablename__ = "mock"
  __mapper_args__ = {"eager_defaults": True}
  id: Mapped[int] = mapped_column(primary_key=True)
  path: Mapped[str] = mapped_column(String(256), unique=True)
  method: Mapped[int] = mapped_column(Integer, default=0xffff)
  content: Mapped[str] = mapped_column(Text, default=b"")
  status_code: Mapped[int] = mapped_column(Integer, default=200)
  headers: Mapped[Dict[str, str]] = mapped_column(JSON, default={"content-type": "text/html"})
  
  def check_method(self, method: str) -> bool:
    method_v = HTTP_METHODS[method]
    return bool(self.method & method_v)
  
  def set_method(self, methods: Union[str, List[str]]):
    "出现即为True"
    if isinstance(methods, str):
      methods = [methods]
    
    self.method = 0
    for method in methods:
      method_v = HTTP_METHODS[method]
      self.method |= method_v
    
    return self
  
  def get_method(self) -> List[str]:
    "返回所有method"
    methods = []
    for method, val in HTTP_METHODS.items():
      if self.method & val:
        methods.append(method)
    return methods
  
  # def get_method_status(self) -> Dict[str, bool]:
  #   "用键值对返回所有method的状态"
  #   ret = {}
  #   for method, val in HTTP_METHODS.items():
  #     ret[method] = bool(self.method & val)
  #   return ret