import os
import json
from httpx import Client, AsyncClient
import pytest
from pytest import fixture
from faker import Faker
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Session
from app import settings
from app.core.db import engine
from app.main import app
from unittest.mock import Mock


@fixture(scope="session")
def db_url():
    # https://stackoverflow.com/a/48234567
    return "postgresql+psycopg2://toubib:toubibPass123@0.0.0.0:5433/toubibdb_test"


@fixture
def sqla_modules():
    pass


@fixture(scope="session")
def faker():
    return Faker()


@fixture
async def client():
    async with AsyncClient(
            app=app,
            base_url=f"http://{settings.api_v1_prefix}"
    ) as client:
        yield client


@fixture(scope="function")
def session() -> Session:
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with session() as s:
        with engine.begin() as conn:
            conn.run_callable(SQLModel.metadata.create_all)

        yield s

    with engine.begin() as conn:
        conn.run_callable(SQLModel.metadata.drop_all)

    engine.dispose()


@fixture(scope="function")
def test_data() -> dict:
    path = os.getenv('PYTEST_CURRENT_TEST')
    path = os.path.join(*os.path.split(path)[:-1], "data", "data.json")

    if not os.path.exists(path):
        path = os.path.join("data", "data.json")

    with open(path, "r") as file:
        data = json.load(file)

    return data

@fixture
def mocker():
    return Mock()
