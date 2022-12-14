import os
import sys
from typing import Any
from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from core.config import settings
from tests.utils.user import authentication_token_from_email

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.base import Base
from db.session import get_db
from apis.base import api_router


def start_application():
    app = FastAPI()
    app.include_router(api_router)
    return app


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def app() -> Generator:
    '''
    This fixture is used to create a new instance for each test.
    '''
    Base.metadata.create_all(bind=engine)
    _app = start_application()
    yield _app
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(
    app: FastAPI, db_session: SessionTesting
) -> Generator[TestClient, Any, None]:
    def _get_test_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
def normal_user_token_headers(client: TestClient, db_session: SessionTesting):
     return  authentication_token_from_email(
        client=client, email=settings.TEST_USER_EMAIL, db=db_session
    )
    
