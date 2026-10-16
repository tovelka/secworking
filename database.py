from flask_sqlalchemy import SQLAlchemy

from config import Config

db_host, db_port, db_name, db_user, db_pass = (
    Config.DB_HOST,
    Config.DB_PORT,
    Config.DB_NAME,
    Config.DB_USER,
    Config.DB_PASSWORD,
)
if not all((db_host, db_port, db_name, db_user, db_pass)):
    raise ValueError('database.py: db_parameters import error.')
DATABASE_URL = (
    f'postgresql+psycopg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
)


db = SQLAlchemy()
