import time
from typing import *
import os
from uuid import uuid4
import logging as lg

from crawlerdetect import CrawlerDetect
import numpy as np
from redis.asyncio import Redis
import uvicorn
from aiofiles import open as aopen
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse

lg.root.setLevel(lg.NOTSET)
DEBUG = False

Time = float

app = FastAPI(docs_url=None, redoc_url=None, debug=False)
redis = Redis(host='redis', port=6379, db=0)

BOMB: Response
SMALL_BOMB: Response
# SCANNER_PATHS: set[str]

def p(arg):
  print(arg)
  return arg

async def get_bomb_rsp(path: str):
  async with aopen(path, "rb") as f:
    content = await f.read()
  return Response(content = content, headers={'Content-Encoding': "br"}, media_type="text/html")

@app.on_event('startup')
async def init_bomb():
  global BOMB, SMALL_BOMB
  BOMB = HTMLResponse("bomb") if DEBUG else await get_bomb_rsp("./bomb.br")
  SMALL_BOMB = HTMLResponse("small bomb") if DEBUG else await get_bomb_rsp("./small_bomb.br")

# @app.on_event('startup')
# async def init_scanner_paths():
#   global SCANNER_PATHS
#   f = await aopen("dict.txt")
#   paths = await f.readlines()
#   SCANNER_PATHS = set([path.strip() for path in paths])
#   # print(SCANNER_PATHS)

limit_time, limit_count = 30, 10

def check_frequency(access_log: list[Time]):
  return len(access_log) <= limit_count

def check_interval(access_log: list[Time]):
  intervals: list[Time] = [access_log[i] - access_log[i - 1] for i in range(1, len(access_log))]
  return (intervals.__len__()<2 or 
          np.var(intervals) > 0.05)

async def log_ip(ip):
  "如果纪录过多就返回False"
  current_time = time.time()

  access_key = f"access:{ip}"
  async with redis.pipeline() as pipe:
    pipe.zadd(access_key, {str(current_time): current_time})
    pipe.zremrangebyscore(access_key, 0, current_time - limit_time)
    pipe.zrange(access_key, 0, -1)
    access_log: list[Time] = [float(t) for t in (await pipe.execute())[-1]]
    if not (check_frequency(access_log) and check_interval(access_log)):
      return False
    
    return True

async def add_session(rsp: Response):
  session = uuid4().__str__()
  rsp.set_cookie("session", session)
  await redis.set(f"session:{session}", 0)
  return rsp

@app.middleware("http")
async def slowAPI(req: Request, call_next):
  if req.url.path in ('/', '/bomb', '/small_bomb'):
    return await call_next(req)
  
  session = req.cookies.get("session", None)
  ip: str = req.client.host
  
  if CrawlerDetect(req.headers, req.headers.get('User-Agent', '')).isCrawler():
    lg.info(f"{ip} is a crawler")
    return BOMB
  if session is None or (await redis.get(f"session:{session}")) is None:
    lg.info(f"{ip} has wrong session")
    return BOMB
  if not await log_ip(ip):
    lg.info(f"{ip} is too fast")
    return BOMB
  
  rsp: Response = await call_next(req)
  rsp = await add_session(rsp)
  await redis.delete(f"session:{session}")
  lg.info(f'{ip} has visited {req.url.path}')
  return rsp

@app.get("/symfony/config/databases.yml")
async def flag():
  return "r00t2023{Wh@t'5 run vvItH mi mem0re?}"

@app.get('/small_bomb')
async def give_u_small_bomb():
  return SMALL_BOMB

@app.get('/bomb')
async def give_u_bomb():
  return BOMB

@app.get('/')
async def root():
  return await add_session(HTMLResponse("Hi!"))

if __name__ == "__main__":
  uvicorn.run(app="app:app", host="0.0.0.0", port=8080, workers=4)
