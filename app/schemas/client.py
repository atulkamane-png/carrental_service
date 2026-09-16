import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


class ClientCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    password: str


class ClientLogin(BaseModel):
    email: EmailStr
    password: str


class ClientOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    full_name: str
    email: EmailStr
    phone: str
    kyc_status: str
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
