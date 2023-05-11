from typing import *
import os
import tarfile
import asyncio as ai
from uuid import uuid4
import re

from httpx import AsyncClient
from jinja2 import Template
from fastapi import Query, Body, Path, Cookie, Depends, UploadFile, File
from fastapi import APIRouter, Request, Response
from fastapi import HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..conf import AMIS_TEMPLATE, SET_AMIS, read_conf, HEADERS
from ..model import AmisRes, AmisExp
from ..sql import Amis, User, MockInfo, PhishTemplate, commit, db_sess, flush, get_session


MOCK_CONF = read_conf("mock")
MOCK_PASSWORD: str = MOCK_CONF['password'] # type: ignore
PLATFORM_SERVER = 'https://r00t.whalecloud.online:8443'

main = APIRouter(tags=["main"])

@main.get('/admin')
async def get_login():
  return RedirectResponse("/amis/pages/admin")

@main.post("/admin")
async def login(username: str = Body(...), 
                password: str = Body(...)):
  if username != "admin":
    raise AmisExp("用户名错误")
  if password != "qwertyui":
    raise AmisExp("密码错误")
  rsp = JSONResponse({"status": 0, "msg": "登录成功"})
  rsp.set_cookie("mock_pass", MOCK_PASSWORD)
  return rsp

@main.get("/static")
async def static_file(path: str = Query("")):
  path = path.replace("../", "")
  return FileResponse("src/static/"+path)

@main.get("/www.zip")
async def flag1():
  return "r00t2023{哇偶, 是flag1! 恭喜你~}"

@main.post("/upload")
def upload(file: UploadFile = File(...)):
  with tarfile.open(fileobj=file.file, mode="r:gz") as tar:
    folder = uuid4().hex
    tar.extractall(path="src/static/upload/"+folder+"/")
    return AmisRes(msg_timeout=30000, data={"path": "/phish/"+folder})

@main.post("/phish/give_me_password")
async def phish0(mail: str = Body(...), 
                 password: str = Body(...),
                 sess: AsyncSession = Depends(db_sess)):
  sess.add(User(username=mail, password=password))


@main.post("/service/auth/normal/login")
async def phish1(mail: str = Body(...), 
                 password: str = Body(...),
                 sess: AsyncSession = Depends(db_sess)):
  async with AsyncClient() as cli:
    rsp = await cli.post(f"{PLATFORM_SERVER}/service/auth/normal/login", json={"mail": mail, "password": password})
    if rsp.status_code==200:
      return rsp.json()
    else:
      rsp = await cli.post(f"{PLATFORM_SERVER}/service/wish/submit_flag?tabid=xTmm", json={'challenge_key': "-1", 'flag': "r00t2023{什么什么? 真有啊......}"}, headers={'x-wish-version': 'wish.2022.v1'})
      # print(rsp.text)
      return {"status": 1, "message": "r00t2023{什么什么? 真有人被钓啊......}"}

template_pt = re.compile(r"{{.*}}")

@main.post("/template")
async def ssti(html: str = Body(..., embed=True),
               sess: AsyncSession = Depends(db_sess),):
  tp = re.findall(template_pt, html)
  for each in tp:
    if each != '{{phish_url}}':
      raise AmisExp("模板只能是{{phish_url}}!")
  path = uuid4().hex
  sess.add(PhishTemplate(path=path, html=html))
  return AmisRes(f"模板路径: /t/{path}", msg_timeout=30000)

@main.get("/t/{path:path}")
async def get_template(path: str = Path(...),
                       sess: AsyncSession = Depends(db_sess),):
  html = await sess.scalar(select(PhishTemplate.html).filter_by(path=path))
  if html is None:
    return Response(status_code=404)
  return HTMLResponse(Template(html.replace("{{phish_url}}", "/phish/give_me_password")).render())

@main.api_route('/{path:path}', 
                methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD'])
async def get_mock(path: str, 
                   req: Request,
                   sess: AsyncSession = Depends(db_sess),):
  mock_info = await sess.scalar(
    select(MockInfo).filter_by(path=path))
  if not mock_info or not mock_info.check_method(req.method):
    return Response(status_code=404)
  return Response(mock_info.content,
                  mock_info.status_code,
                  mock_info.headers,)
