import uuid
from sqlalchemy import Column, String, DateTime, DECIMAL
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.sql import func
from app.db.base import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    full_name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    kyc_status = Column(String(20), default="pending")
    license_number = Column(String(50), nullable=True)
    license_doc_url = Column(String(500), nullable=True)
    risk_score = Column(DECIMAL(4, 2), default=0.0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
