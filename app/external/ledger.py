import asyncio

async def update_ledger(data):
    """ mock ledger function """
    await asyncio.sleep(0.3)
    print(
        f"Ledger updated for transfer {data}"
    )