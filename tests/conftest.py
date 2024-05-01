"""App Module: Testing Configuration."""

from re import compile as regex_compile
from typing import Any
from pytest import fixture
from sqlalchemy.orm import Session
from config import AppConfig


@fixture
def app() -> AppConfig:
    """Initializes the Application Config."""

    return AppConfig()


def setup_test_commit(model: Any, session: Session):
    """Abstraction of the persistence functionality."""

    session.add(model)
    session.commit()


def run_test_teardown(private_id: str, model: Any, session: Session):
    """Abstraction of the Clearing of the Test Database."""

    model = session.get(model, private_id)
    session.delete(model)
    session.commit()


def get_id_by_regex(value: str) -> str:
    """Get Model ID By Regex."""

    regex = regex_compile(r"^.*: (.*)$")
    regex_match = regex.match(value)
    assert regex_match is not None
    matches = regex_match.groups()
    assert regex_match is not None
    assert len(matches) == 1
    return matches[0]
