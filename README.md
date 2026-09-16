# User Service — AI Car Rental Platform

FastAPI microservice handling client signup, login, and profile — connects to Azure SQL (`CarRentalCore` database).

## Setup on your VM (Ubuntu)

```bash
# 1. Install system dependencies
sudo apt update
sudo apt install -y python3-pip python3-venv git curl gnupg2

# 2. Install Microsoft ODBC Driver 18 (required for pyodbc -> Azure SQL)
curl https://packages.microsoft.com/keys/microsoft.asc | sudo tee /etc/apt/trusted.gpg.d/microsoft.asc
curl https://packages.microsoft.com/config/ubuntu/22.04/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list
sudo apt update
sudo ACCEPT_EULA=Y apt install -y msodbcsql18

# 3. Clone your repo (if not already on the VM)
git clone https://github.com/yourname/yourrepo.git
cd yourrepo/services/user-service

# 4. Create virtual environment and install Python packages
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 5. Configure environment variables
cp .env.example .env
nano .env   # fill in your Azure SQL server, username, password, JWT secret

# 6. Test the DB connection BEFORE running the app
python test_connection.py

# 7. Run the app
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Visit `http://<your-vm-ip>:8000/docs` to see the Swagger UI and test the `/signup` and `/login` endpoints.

## Run permanently (survives reboot / SSH disconnect)

```bash
sudo cp user-service.service /etc/systemd/system/user-service.service
sudo nano /etc/systemd/system/user-service.service   # fix the paths + User=
sudo systemctl daemon-reload
sudo systemctl enable user-service
sudo systemctl start user-service
sudo systemctl status user-service
```

## Endpoints included in this MVP

| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/auth/signup` | Create a new client |
| POST | `/api/v1/auth/login` | Login, returns JWT |
| GET | `/api/v1/clients/{id}` | Get client profile |
| GET | `/health` | Health check + DB connectivity check |

## Next services to build (same pattern)

Copy this folder structure for `booking-service`, `vehicle-service`, `payment-service` — each gets its own `app/models`, `app/schemas`, `app/crud`, `app/api` following this exact layout.
