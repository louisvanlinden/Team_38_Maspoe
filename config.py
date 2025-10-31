import os

class Config:
    # 1) DATABASE_URL komt uit omgeving (.env)
    # 2) Valt terug op SQLite (app.db) als DATABASE_URL leeg is
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///app.db")
    # Uitschakelen van een oude, dure feature
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Voor cookies/flash messages; zet later iets sterkers in .env
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
