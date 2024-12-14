from flask import Blueprint, request, jsonify
from http import HTTPStatus
import uuid
from services.player_service import PlayerService
from models.player_profile import PlayerProfile
from utils.validators import validate_player_data
from utils.error_handler import handle_errors
from exceptions import PlayerNotFoundError

players_bp = Blueprint('players_bp', __name__, url_prefix='/v1/players')

@players_bp.route('', methods=['GET'])
def get_players():
    player_service = PlayerService()
    result = player_service.get_all_players()
    return jsonify(result)

@players_bp.route('/<string:player_id>')
@handle_errors
def query_player_id(player_id):
    player_service = PlayerService()
    result = player_service.search_by_player(player_id)

    if not result:
        return jsonify({"error": f"No record found with player_id={player_id}"}), HTTPStatus.NOT_FOUND
    else:
        return jsonify(result)

@players_bp.route('', methods=['POST'])
@handle_errors
def create_player():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['nameFirst', 'nameLast']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                'error': 'Missing required fields',
                'missing_fields': missing_fields
            }), HTTPStatus.BAD_REQUEST
        
        # Generate unique player ID if not provided
        if 'playerId' not in data:
            data['playerId'] = f"PL{uuid.uuid4().hex[:8].upper()}"
            
        # Validate data types
        validation_error = validate_player_data(data)
        if validation_error:
            return jsonify({
                'error': 'Invalid data format',
                'details': validation_error
            }), HTTPStatus.BAD_REQUEST
            
        # Create PlayerProfile instance
        try:
            player = PlayerProfile.from_dict(data)
        except ValueError as e:
            return jsonify({
                'error': 'Invalid player data',
                'details': str(e)
            }), HTTPStatus.BAD_REQUEST
            
        # Insert into database
        player_service = PlayerService()
        if player_service.check_duplicate_player(player.to_dict()):
            return jsonify({
                'status': 'error',
                'message': 'Duplicate Error: Player already exists in the database'
            }), HTTPStatus.CONFLICT
        
        player_service.insert_player(player.to_dict())
        return jsonify({
            'message': 'Player created successfully',
            'playerId': player.playerId,
            'player': player.to_dict()
        }), HTTPStatus.CREATED
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), HTTPStatus.INTERNAL_SERVER_ERROR
    
@players_bp.route('/<string:player_id>', methods=['PATCH'])
@handle_errors
def partial_update_player(player_id):
    data = request.get_json()

    if not data:
        return jsonify({
            'error': 'No data provided for update'
        }), HTTPStatus.BAD_REQUEST

    # Update the player in the database using the service layer
    player_service = PlayerService()
    if not player_service.player_exists(player_id):
        raise PlayerNotFoundError(f"No player found with playerId {player_id}")

    player_service.partial_update_player(player_id, data)
    return jsonify({
        'message': 'Player updated successfully',
        'playerId': player_id
    }), HTTPStatus.OK