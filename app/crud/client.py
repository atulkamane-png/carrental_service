from sqlalchemy.orm import Session
from app.models.client import Client
from app.schemas.client import ClientCreate
from app.core.security import hash_password


def get_client_by_email(db: Session, email: str) -> Client | None:
    return db.query(Client).filter(Client.email == email).first()


def create_client(db: Session, client_in: ClientCreate) -> Client:
    db_client = Client(
        full_name=client_in.full_name,
        email=client_in.email,
        phone=client_in.phone,
        password_hash=hash_password(client_in.password),
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


def get_client_by_id(db: Session, client_id: str) -> Client | None:
    return db.query(Client).filter(Client.id == client_id).first()
