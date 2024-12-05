import pytest
from services.player_service import PlayerService
from models.player_profile import PlayerProfile
from exceptions import PlayerNotFoundError
from unittest.mock import MagicMock

@pytest.fixture
def player_service(mocker):
    # Mock the database connection and cursor
    mock_conn = mocker.patch('services.player_service.sqlite3.connect')
    mock_cursor = MagicMock()
    mock_conn.return_value.cursor.return_value = mock_cursor
    service = PlayerService()
    service.cursor = mock_cursor
    return service

def test_search_by_player_found(player_service):
    # Mock the database response
    player_service.cursor.fetchone.return_value = {
        'playerId': 'PL123456',
        "nameFirst": "TestLife",
        "nameLast": "Cycle",
        "birthYear": 1990,
        "birthMonth": 6,
        "birthDay": 15,
        "birthCountry": "USA",
        "birthState": "CA",
        "birthCity": "Los Angeles"
    }

    result = player_service.search_by_player('PL123456')
    assert result['playerId'] == 'PL123456'
    assert result['nameFirst'] == 'TestLife'
    assert result['nameLast'] == 'Cycle'

def test_search_by_player_not_found(player_service):
    # Mock the database response
    player_service.cursor.fetchone.return_value = None

    with pytest.raises(PlayerNotFoundError):
        player_service.search_by_player('PL000000')