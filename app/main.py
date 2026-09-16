from fastapi import FastAPI
from app.api.v1.endpoints import clients, auth
from app.db.session import engine
from app.models import client as client_model

# Auto-create tables on startup (fine for dev; use Alembic migrations for prod)
client_model.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="User Service - AI Car Rental Platform",
    version="0.1.0",
    description="Handles client signup, login, and KYC status."
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(clients.router, prefix="/api/v1/clients", tags=["clients"])


@app.get("/")
def root():
    return {"service": "user-service", "status": "running"}


@app.get("/health")
def health_check():
    """Simple health check - also verifies DB connectivity."""
    try:
        with engine.connect() as conn:
            conn.exec_driver_sql("SELECT 1")
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    return {"status": "ok", "database": db_status}
