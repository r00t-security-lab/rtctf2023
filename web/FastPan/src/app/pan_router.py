from fastapi import FastAPI, APIRouter
from uvicorn import run
from fastapi import Body, Query, Depends, Response, Cookie, File, Form, Path as Path2, UploadFile
from fastapi.responses import RedirectResponse, FileResponse
from ..sql import User, uFile, user_file, db_sess, commit
from sqlalchemy import delete, insert, select, text, update
from sqlalchemy.ext.asyncio import AsyncSession
from ..model import AmisRes, AmisExp
from pathlib import Path
import jwt
from hashlib import md5
import aiofiles
from urllib.parse import quote
pan = APIRouter()


class exp(Exception):
    pass


def logined(filepath: str = Cookie(None)):
    if filepath:
        user = jwt.decode(filepath, key="r00tctf2023",
                          algorithms=["HS256"])['user']
        if user=='pyy':
            raise AmisExp(msg="pyy整天乱搞, 现在我宣布pyy被封号了")
        return user


@pan.get("/money")
def money():
    return FileResponse("src/static/money.jpg")


@pan.post('/register')
async def register(res: Response, uname: str = Body(...), passwd: str = Body(...), db: AsyncSession = Depends(db_sess)):

    raise AmisExp("给koali打钱！谢谢！")
    user = User(uname=uname, passwd=passwd)
    db.add(user)
    if await commit(catch_regex=r"\(1062,"):
        return AmisRes(msg="注册成功")
    else:
        return AmisRes(status=1, msg="用户名重复")


@pan.get('/login')
def getlogin():
    return "please post"


@pan.post('/login')
async def login(res: Response, uname: str = Body(...), passwd: str = Body(...), db: AsyncSession = Depends(db_sess)):
    try:
        ans = await db.scalar(text(f"Select uname from User where uname = '{uname}' and passwd = '{passwd}';"))
        if uname=='pyy':
            return AmisRes(status=1, msg="pyy整天乱搞, 现在我宣布pyy被封号了")
        if ans:
            filepath = jwt.encode({"user": ans}, "r00tctf2023", algorithm="HS256")
            res.set_cookie("filepath", filepath)
            return AmisRes(msg="登录成功")
        return AmisRes(status=1, msg="你要不注册试试？")
    except Exception as e:
        return AmisRes(status=1, msg=e.__repr__())


@pan.post("/upload")
async def upload(file: UploadFile, db: AsyncSession = Depends(db_sess), uname=Depends(logined), md5_res: str = Body(...)):
    filepath = md5(uname.encode('utf-8')).hexdigest()
    Path('upload').joinpath(filepath).mkdir(parents=True, exist_ok=True)
    file_content = (await file.read())

    ufile = uFile(filename=file.filename, fileMD5=md5_res)
        
    #ufile = uFile(filename=file.filename, fileMD5=md5(file_content.replace(b'\r\n', b'\n')).hexdigest())
    user = await db.scalar(select(User).filter_by(uname=uname))
    assert user is not None, "什么什么，我jwt又被破解了QAQ！！！"
    db.add(ufile)
    ufile.users.append(user)
    if(Path(ufile.path).exists()):
        raise AmisExp("文件已存在")
    if await commit(catch_regex=r"\(1062,"):
        async with aiofiles.open(ufile.path, 'wb') as f:
            await f.write(file_content)
            return AmisRes(status=0, msg="上传成功", data={"value": "success!!!!!!!!!!!!!!!!!!!!!"})
    else:
        raise AmisExp("未知错误喵~")


@pan.get("/filelist")
async def filelist(db: AsyncSession = Depends(db_sess), uname=Depends(logined)):
    if uname is None:
        return RedirectResponse("/pan/login")
    user = await db.scalar(select(User).filter_by(uname=uname))
    assert user is not None, "什么什么，我jwt被破解了QAQ！！！"
    # print(user.files)
    return user.files


@pan.get("/filedownload")
async def filedownload(db: AsyncSession = Depends(db_sess), uname=Depends(logined), filename: str = Query(...)):
    if(not uname):
        return RedirectResponse("/pan/login")
    file = await db.scalar(select(uFile).filter_by(filename=filename))
    assert file is not None, "文件木大啦"

    return FileResponse(path=file.path, status_code=200, headers={"Content-Disposition": f'attachment; filename="{quote(filename)}"'})


@pan.get("/filedelete")
async def filedelete(db: AsyncSession = Depends(db_sess), uname=Depends(logined), filename: str = Query(...)):
    if(not uname):
        return RedirectResponse("/pan/login")
    if filename.startswith("flag"):
        return AmisRes(status=1, msg="咦,文件删不掉耶")
    filepath = Path("upload/"+md5(uname.encode('utf-8')
                                  ).hexdigest()+"/"+filename)
    FileDelete = await db.execute(delete(uFile).filter_by(filename=filename))
    # print("输出在这里喵",[FileDelete[x] for x in FileDelete.fetchall()])
    # 一切问题遇到pyy迎刃而解
    assert FileDelete.rowcount > 0, "咦,文件删不掉耶"
    filepath.unlink()
    return AmisRes(status=0, msg="删除成功喵~")


@pan.get("/秒传")
async def fast_upload(db: AsyncSession = Depends(db_sess),
                      file_md5: str = Query(..., alias='md5'),
                      filename: str = Query(...),
                      uname=Depends(logined)):
    if(not uname):
        return RedirectResponse("/pan/login")
    filepath = md5(uname.encode('utf-8')).hexdigest()
    Path('upload').joinpath(filepath).mkdir(parents=True, exist_ok=True)
    file = await db.scalar(select(uFile).filter_by(fileMD5=file_md5))
    if file is not None:
        new_file = uFile(filename=filename, fileMD5=file.fileMD5)
        user = await db.scalar(select(User).filter_by(uname=uname))
        assert user is not None, "什么什么，我jwt又被破解了QAQ！！！"
        db.add(new_file)
        new_file.users.append(user)
        try:
            file.path.link_to(new_file.path)
        except:
            raise AmisExp("文件存在了耶", status=0)
        return AmisRes("秒传成功! 是不是炒鸡快!")
    raise AmisExp()


@pan.get("/secret")
async def secret():
    return AmisRes(status=0, msg="被你发现啦！")
