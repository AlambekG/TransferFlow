from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Account(Base):
    id
    client_id
    balance
    currency

class Transfer(Base):
    id
    from_account
    to_account
    amount
    status