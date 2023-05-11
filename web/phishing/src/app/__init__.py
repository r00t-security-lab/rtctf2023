from .amis_router import amis
from .mock_router import mock
from .main_router import main

async def startup():
  from asyncio import gather
  from .amis_router import load_pages, generate_sdk
  
  await gather(load_pages(), generate_sdk())
