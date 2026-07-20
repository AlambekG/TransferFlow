import enum
import uuid

from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    Enum,
    ForeignKey,
    TIMESTAMP,
    func,
)

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.dialects.postgresql import UUID


class Base(DeclarativeBase):
    pass


class TransferStatusEnum(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)

    uuid = Column(
        UUID(as_uuid=True),
        unique=True,
        nullable=False,
        default=uuid.uuid4
    )

    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True)

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now()
    )


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True)

    client_id = Column(
        Integer,
        ForeignKey("clients.id"),
        nullable=False
    )

    balance = Column(
        Numeric(18, 2),
        nullable=False,
        default=0
    )

    currency = Column(
        String(3),
        nullable=False
    )

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now()
    )


class Transfer(Base):
    __tablename__ = "transfers"

    id = Column(Integer, primary_key=True)

    idempotency_key = Column(
        UUID(as_uuid=True),
        unique=True,
        nullable=False,
        default=uuid.uuid4
    )

    from_account_id = Column(
        Integer,
        ForeignKey("accounts.id"),
        nullable=False
    )

    to_account_id = Column(
        Integer,
        ForeignKey("accounts.id"),
        nullable=False
    )

    amount = Column(
        Numeric(18, 2),
        nullable=False
    )

    status = Column(
        Enum(TransferStatusEnum),
        nullable=False,
        default=TransferStatusEnum.PENDING
    )

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now()
    )