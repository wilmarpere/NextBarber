from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # App
    APP_NAME: str = "NextBarber"
    DEBUG: bool = True

    # Database (SQLite para desarrollo, PostgreSQL para producción)
    DATABASE_URL: str = "sqlite:///./nextbarber.db"

    # JWT
    SECRET_KEY: str = "tu-secret-key-super-segura-cambiar-en-produccion"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    # Mapbox
    MAPBOX_ACCESS_TOKEN: str = ""

    # Stripe
    STRIPE_SECRET_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""

    # ePayco
    EPAYCO_PUBLIC_KEY: str = ""
    EPAYCO_PRIVATE_KEY: str = ""

    # Firebase
    FIREBASE_CREDENTIALS_PATH: str = ""

    # Cloudinary
    CLOUDINARY_CLOUD_NAME: str = ""
    CLOUDINARY_API_KEY: str = ""
    CLOUDINARY_API_SECRET: str = ""

    # WhatsApp (Twilio)
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_WHATSAPP_NUMBER: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
