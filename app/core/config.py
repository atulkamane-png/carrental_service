from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Azure SQL / SQL Server connection details
    DB_SERVER: str          # e.g. yourserver.database.windows.net
    DB_NAME: str = "CarRentalCore"
    DB_USER: str
    DB_PASSWORD: str
    DB_DRIVER: str = "ODBC Driver 18 for SQL Server"

    # Auth
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    @property
    def DATABASE_URL(self) -> str:
        driver_encoded = self.DB_DRIVER.replace(" ", "+")
        return (
            f"mssql+pyodbc://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_SERVER}:1433/{self.DB_NAME}"
            f"?driver={driver_encoded}&Encrypt=yes&TrustServerCertificate=no"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
