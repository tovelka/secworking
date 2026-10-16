"""Конфигурация приложения: настройки берутся из переменных окружения (.env)."""

import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Настройки подключения к PostgreSQL."""

    DB_HOST: str = os.getenv('DB_HOST', 'localhost')
    DB_PORT: int = int(os.getenv('DB_PORT', '5432'))
    DB_USER: str = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD', '')
    DB_NAME: str = os.getenv('DB_NAME', 'notes_db')
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'secret-key')
