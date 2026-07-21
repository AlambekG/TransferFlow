import asyncio

async def check_transfer(from_id, to_id, amount):
    """ mock fraud detection. currently just return true"""
    await asyncio.sleep(0.3)
    return True