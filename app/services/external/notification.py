import asyncio
from app.services.retries import retry

@retry(3)
async def send_notification(data):
    """ mock notification service """
    await asyncio.sleep(0.3)
    print(
        f"Notification sent for transfer {data}"
    )