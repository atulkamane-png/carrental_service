"""
Run this BEFORE starting the full app to confirm:
  1. The ODBC driver is installed correctly
  2. Your VM's IP is whitelisted in Azure SQL firewall
  3. Your credentials in .env are correct

Usage:
    python test_connection.py
"""
from app.core.config import settings
from sqlalchemy import create_engine, text

print(f"Connecting to {settings.DB_SERVER}/{settings.DB_NAME} ...")

try:
    engine = create_engine(settings.DATABASE_URL)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1 AS test_value"))
        row = result.fetchone()
        print(f"✅ Connection successful. Test query returned: {row}")

        # Bonus: confirm the clients table exists (created by CarRentalCore schema)
        tables = conn.execute(text(
            "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'"
        )).fetchall()
        print(f"📋 Tables found in {settings.DB_NAME}: {[t[0] for t in tables]}")

except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("\nCheck: 1) VM IP whitelisted in Azure SQL firewall  "
          "2) ODBC Driver 18 installed  3) .env values correct")
