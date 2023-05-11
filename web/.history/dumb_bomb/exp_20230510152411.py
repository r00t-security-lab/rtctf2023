# 炸弹指的是gzip炸弹, 但是会返回br结果, 如果直接爬取会出问题
# 反爬手段: 1. 限制同ip访问频率(访问间隔是否固定, 30秒内是否超过10次) 2. 检测ua 3. 检测cookie
# 反制手段: 1. 慢慢爬/ip池 2. 使用浏览器ua 3. 使用requests.Session

from random import random as rd
from time import sleep
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

import requests
from pitricks.utils import retry, pwd

URL = 'http://121.5.48.11:20016/'

class SessionWrong(Exception):
  pass

def get_dict():
  with open(pwd()/'dict.txt') as f:
    return [line.strip() for line in f.readlines()]

def init_session():
  sess = requests.Session()
  sess.get(URL)
  return sess

def craw_one(url: str, sess: requests.Session):
  # print(f"try {url}")
  res = sess.get(
    url, stream=True,
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.68'}, 
    proxies={'http': "http://127.0.0.1:7890"})
  if res.headers.get('content-encoding', None)=='br':
    sleep(rd()*16)
    # print("sleep......")
    raise SessionWrong()
  if res.status_code==502:
    return craw_one(url, sess)
  return res.status_code!=404

progress_bar: tqdm
def craw(paths: list[str]):
  global progress_bar
  sess = init_session()
  for path in paths:
    while True:
      try:
        if craw_one(URL+path, sess):
          print(path)
        break
      except requests.exceptions.ConnectionError:
        pass
      except SessionWrong:
        sess = init_session()
    
    progress_bar.update()
    sleep(rd()*10)

if __name__=='__main__':
  dic = get_dict()
  progress_bar = tqdm(range(len(dic)))
  pool = ThreadPoolExecutor(80)
  [f.result()
   for f in [pool.submit(craw, dic[i:i+20]) 
             for i in range(0, len(dic), 20)]]