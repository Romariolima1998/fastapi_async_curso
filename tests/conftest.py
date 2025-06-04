from datetime import datetime
from contextlib import contextmanager

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import event

from fastapi_zero.app import app
from fastapi_zero.models import table_registry

from fastapi_zero.models import User

import pytest




@pytest.fixture
def client():

    return TestClient(app)

@pytest.fixture
def session():

    engine = create_engine('sqlite:///:memory:', echo=True)
    table_registry.metadata.create_all(engine)
    with Session(engine) as session:

        yield session
        table_registry.metadata.drop_all(engine)

        table_registry.metadata.drop_all(engine)

@contextmanager
def _mock_db_time(model= User, time= datetime.now()):
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
        
    event.listen(model, 'before_insert', fake_time_hook)

    yield time

    event.remove(model, 'before_insert', fake_time_hook)

@pytest.fixture
def mock_db_time():
    return _mock_db_time