from .amis_router import amis
from .pan_router import pan

async def startup():
  from .amis_router import load_pages
  await load_pages()
