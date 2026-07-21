import asyncio

async def send_notification(data):
    """ mock notification service """
    await asyncio.sleep(0.3)
    print(
        f"Notification sent for transfer {data}"
    )