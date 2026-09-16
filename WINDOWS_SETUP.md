# User Service — Windows VM Setup Guide

Same FastAPI project as before, adapted for a **Windows Server VM** on Azure.

## 1. Install prerequisites on the VM (via RDP)

1. **Python** — download from https://www.python.org/downloads/ (get 3.12.x).
   During install, **check "Add python.exe to PATH"** — easy to miss, causes `python` not recognized later.
2. **Git** — download from https://git-scm.com/download/win, install with defaults.
3. **ODBC Driver 18 for SQL Server** — download the `.msi` from:
   https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
   Run it, accept defaults.
4. **SSMS** (optional but handy since you're already using it) — install directly on the VM so you can manage the DB without hopping back to your laptop.

Verify in Command Prompt or PowerShell:
```powershell
python --version
git --version
```

## 2. Clone your repo

```powershell
cd C:\
mkdir apps
cd apps
git clone https://github.com/yourname/yourrepo.git
cd yourrepo\services\user-service
```

## 3. Create virtual environment and install dependencies

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

(Note the backslash — Windows activation differs from Linux's `source venv/bin/activate`.)

## 4. Configure environment variables

```powershell
copy .env.example .env
notepad .env
```
Fill in `DB_SERVER`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `JWT_SECRET_KEY`.

## 5. Test the DB connection

```powershell
python test_connection.py
```
You should see `✅ Connection successful.` If not, check the Azure SQL firewall rule (Step-by-step guide covers this) and that the ODBC driver installed correctly.

## 6. Run the app manually (for testing)

```powershell
venv\Scripts\uvicorn app.main:app --host 0.0.0.0 --port 8000
```
Visit `http://<vm-public-ip>:8000/docs` from your own browser once the port is open (see connection steps guide).

## 7. Keep it running permanently — using NSSM

Windows has no built-in equivalent to Linux's `systemd`, so we use **NSSM** (Non-Sucking Service Manager), a free, widely-used tool that wraps any command into a real Windows Service — auto-starts on boot, auto-restarts on crash.

```powershell
# Download NSSM from https://nssm.cc/download, extract it, e.g. to C:\nssm

# Install the service (run in an elevated/Administrator PowerShell)
C:\nssm\win64\nssm.exe install UserService

# A GUI window opens — fill in:
#   Path:             C:\apps\yourrepo\services\user-service\venv\Scripts\uvicorn.exe
#   Startup directory: C:\apps\yourrepo\services\user-service
#   Arguments:         app.main:app --host 0.0.0.0 --port 8000

# Then start it:
nssm start UserService

# Check status:
nssm status UserService

# View logs: configure the "I/O" tab in the NSSM GUI to redirect
# stdout/stderr to a log file, e.g. C:\apps\logs\user-service.log
```

To stop/remove later:
```powershell
nssm stop UserService
nssm remove UserService confirm
```

## Endpoints (same as before)

| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/auth/signup` | Create a new client |
| POST | `/api/v1/auth/login` | Login, returns JWT |
| GET | `/api/v1/clients/{id}` | Get client profile |
| GET | `/health` | Health check + DB connectivity check |
