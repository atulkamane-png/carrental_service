from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.client import ClientCreate, ClientLogin, ClientOut, Token
from app.crud import client as client_crud
from app.core.security import verify_password, create_access_token

router = APIRouter()


@router.post("/signup", response_model=ClientOut, status_code=status.HTTP_201_CREATED)
def signup(client_in: ClientCreate, db: Session = Depends(get_db)):
    existing = client_crud.get_client_by_email(db, client_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return client_crud.create_client(db, client_in)


@router.post("/login", response_model=Token)
def login(credentials: ClientLogin, db: Session = Depends(get_db)):
    client = client_crud.get_client_by_email(db, credentials.email)
    if not client or not verify_password(credentials.password, client.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_access_token({"sub": str(client.id)})
    return Token(access_token=token)
