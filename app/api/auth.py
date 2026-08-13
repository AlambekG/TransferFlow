from fastapi import Header, HTTPException


async def get_current_client(x_client_id: int | None = Header(None, alias="X-Client-Id")) -> int:
    if x_client_id is None:
        raise HTTPException(status_code=401, detail="Missing X-Client-Id header")
    try:
        return int(x_client_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid X-Client-Id header")
