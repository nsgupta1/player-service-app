import pytest
from app import create_app
from database.init_db import initialize_database

@pytest.fixture(scope='session')
def app():
    # Setup
    app = create_app()
    app.config['TESTING'] = True
    app.config['DEBUG'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://test_player.db'

    # Initialize the test database
    initialize_database(db_file='test_player.db')

    yield app

    # Teardown
    # Remove the test database file if necessary

@pytest.fixture(scope='session')
def client(app):
    return app.test_client()

@pytest.fixture(scope='function')
def runner(app):
    return app.test_cli_runner()