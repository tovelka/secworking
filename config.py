"""Конфигурация приложения: настройки берутся из переменных окружения (.env)."""

import os

from dotenv import load_dotenv

# Загружаем переменные из файла .env (если он есть рядом с проектом)
load_dotenv()


class Config:
    """Настройки подключения к MySQL."""

    DB_HOST: str = os.getenv('DB_HOST', 'localhost')
    DB_USER: str = os.getenv('DB_USER', 'root')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD', '')
    DB_NAME: str = os.getenv('DB_NAME', 'notes_db')
