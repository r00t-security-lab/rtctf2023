from typing import *
import asyncio as ai

from fastapi import Query, Body, Path, Cookie, Depends
from fastapi import APIRouter, Request, Response
from fastapi import HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..conf import read_conf
from ..model import AmisRes, AmisExp
from ..sql import MockInfo
from ..sql import commit, db_sess, flush, get_session

MOCK_CONF = read_conf("mock")
ADMIN_PASSWORD: str = MOCK_CONF['password'] # type: ignore


async def admin_check(mock_pass: str = Cookie("")):
  if mock_pass != ADMIN_PASSWORD:
    raise HTTPException(status_code=404)

mock = APIRouter(tags=["mock"])
mock_admin = APIRouter(dependencies=[Depends(admin_check)])

@mock_admin.get('/path')
async def get_path(sess: AsyncSession = Depends(db_sess)):
  paths = await sess.scalars(select(MockInfo.path))
  return {'options': [{"label": path, "value": path}
                      for path in paths]}

@mock_admin.get('/all_pages')
async def get_all_pages(sess: AsyncSession = Depends(db_sess)):
  pages = await sess.scalars(select(MockInfo))
  return {"data": {"paths": {
    page.path: {
      "status_code": page.status_code, 
      "method": page.get_method(),
      "status_code": page.status_code,
      "headers": page.headers,
      "content": page.content,} 
    for page in pages}}}
  
@mock_admin.post('/path')
async def create_path(path: str = Body(..., embed=True), 
                      sess: AsyncSession = Depends(db_sess)):
  sess.add(MockInfo(path=path))
  if await commit(catch_regex=r"\(1062,"):
    return AmisRes("创建成功")
  else:
    raise AmisExp("路径重复")

@mock_admin.patch('/path')
async def update_path(origin: str = Body(...), replace_as: str = Body(...), 
                      sess: AsyncSession = Depends(db_sess)):
  await sess.execute(
    update(MockInfo).where(MockInfo.path==origin).values(path=replace_as))
  if await commit(catch_regex=r"\(1062,"):
    return AmisRes("修改成功")
  else:
    raise AmisExp("路径重复")

@mock_admin.delete('/path')
async def delete_path(path: str = Body(..., embed=True), 
                      sess: AsyncSession = Depends(db_sess)):
  await sess.execute(
    delete(MockInfo).where(MockInfo.path==path))
  await commit(echo=True)
  return AmisRes("删除成功")

@mock_admin.post('/set_pages')
async def set_amis(path: str = Body(...), 
                   method: List[str] = Body(...),
                   status_code: int = Body(...), 
                   headers: Dict[str, str] = Body(...), 
                   content: str = Body(...),
                   sess: AsyncSession = Depends(db_sess)):
  # 为了兼容其实并不存在的多种数据库, 就不用upsert了
  page = await sess.scalar(
    select(MockInfo).filter_by(path=path))
  if page:
    page.set_method(method)
    page.status_code, page.headers, page.content = status_code, headers, content
  else:
    sess.add(MockInfo(path=path, status_code=status_code, headers=headers, content=content).set_method(method))
  if await commit(echo=True):
    return AmisRes("保存成功")
  else:
    raise AmisExp("保存失败")

mock.include_router(mock_admin)
