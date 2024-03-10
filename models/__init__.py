"""Models Module Entry Point."""

from sqlalchemy.orm import declarative_base
from sqlalchemy.engine import create_engine


ENGINE = create_engine(
    "postgresql://py_user:py_user_password@localhost:5433/py_coin_db"
)

Base = declarative_base()
