from decimal import Decimal
from pydantic import BaseModel, validator


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

    @validator("amount")
    def amount_must_be_positive(cls, v: Decimal):
        try:
            if v <= 0:
                raise ValueError("amount must be greater than 0")
        except TypeError:
            raise ValueError("amount must be a number")
        return v


class TransferResponse(BaseModel):
    id: int
    status: str
    class Config:
        from_attributes = True