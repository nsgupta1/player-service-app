import pytest
from flask import url_for
import random

def test_get_players(client):
    response = client.get('/v1/players')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_create_player(client):
    firstName = generate_unique_name()
    new_player = {
        'nameFirst': str(firstName),
        'nameLast': 'Smith',
        'birthYear': 1995,
        "birthYear": 1990,
        "birthMonth": 6,
        "birthDay": 15,
        "birthCountry": "USA",
        "birthState": "CA",
        "birthCity": "Los Angeles"
    }
    print(f'dict:', new_player)
    response = client.post('/v1/players', json=new_player)
    assert response.status_code == 201
    assert 'playerId' in response.json
    assert response.json['player']['nameFirst'] == firstName

def test_get_player_by_id(client):
    # First, create a player to ensure one exists
    firstName = generate_unique_name(),
    new_player = {
        'nameFirst': str(firstName),
        'nameLast': 'Brown',
        'birthYear': 1990,
        "birthYear": 1990,
        "birthMonth": 6,
        "birthDay": 15,
        "birthCountry": "USA",
        "birthState": "CA",
        "birthCity": "Los Angeles"
    }
    create_response = client.post('/v1/players', json=new_player)
    player_id = create_response.json['playerId']

    # Now, retrieve the player by ID
    response = client.get(f'/v1/players/{player_id}')
    assert response.status_code == 200
    assert response.json['playerId'] == player_id

def test_update_player(client):
    # Create a player to update
    firstName = generate_unique_name
    new_player = {
        'nameFirst': str(firstName),
        'nameLast': 'Davis',
        'birthYear': 1985,
        "birthYear": 1990,
        "birthMonth": 6,
        "birthDay": 15,
        "birthCountry": "USA",
        "birthState": "CA",
        "birthCity": "Los Angeles"
    }
    create_response = client.post('/v1/players', json=new_player)
    player_id = create_response.json['playerId']

    # Update the player's data
    updated_data = {
        'nameFirst': 'Charles',
        'weight': 180
    }
    response = client.patch(f'/v1/players/{player_id}', json=updated_data)
    assert response.status_code == 200

    # Verify the update
    get_response = client.get(f'/v1/players/{player_id}')
    assert get_response.json['nameFirst'] == 'Charles'
    assert get_response.json['weight'] == 180

def generate_unique_name(base_name='player'):
    unique_suffix = random.randint(1000, 9999)
    return f"{base_name}{unique_suffix}"