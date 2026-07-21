from decimal import Decimal
from pydantic import BaseModel


class AccountResponse(BaseModel):
    id: int
    balance: Decimal
    currency: str
    class Config:
        from_attributes = True


class TransferRequest(BaseModel):
    from_account_id: int
    to_account_id: int
    amount: Decimal


class TransferResponse(BaseModel):
    id: int
    status: str
    class Config:
        from_attributes = True