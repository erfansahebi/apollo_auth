import pytest
from nameko.testing.services import worker_factory
from apollo_shared.alembic.models import Base
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.dialects import postgresql
from sqlite3 import Connection as SQLite3Connection
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture(scope='session')
def db_url():
    return 'sqlite:///:memory:'


@pytest.yield_fixture(scope='session')
def db_connection(db_url, model_base, db_engine_options):
    engine = create_engine(db_url, **db_engine_options)
    model_base.metadata.create_all(engine)

    from auth.models.user import user
    user.drop(engine)
    user.create(engine)

    connection = engine.connect()
    model_base.metadata.bind = engine

    yield connection

    engine.dispose()

@pytest.fixture(scope='session')
def model_base():
    return Base


@pytest.fixture(scope='session')
def db_engine_options():
    @event.listens_for(Engine, 'connect')
    def set_sqlite_pragma(dbapi_connection, connection_record):
        if isinstance(dbapi_connection, SQLite3Connection):
            cursor = dbapi_connection.cursor()
            cursor.execute('PRAGMA foreign_keys=ON')
            cursor.close()

    @compiles(postgresql.UUID, 'sqlite')
    def compile_sqlite_uuid(type_, compiler, **kw):
        return 'STRING'

    return {}


@pytest.fixture
def context():
    return {
        'request_id': 'request_id',
        'token': 'token',
        'user_id': '1',
    }


@pytest.fixture
def auth_controller(database):
    from auth.controller import AuthController
    return worker_factory(AuthController, db=database)
