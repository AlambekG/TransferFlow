import asyncio
from app.services.retries import retry

@retry(3)
async def check_transfer(from_id, to_id, amount):
    """ mock fraud detection. currently just return true"""
    await asyncio.sleep(0.3)
    return True