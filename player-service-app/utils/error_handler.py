import logging
from flask import jsonify
from functools import wraps
from http import HTTPStatus
from exceptions import PlayerNotFoundError

logger = logging.getLogger(__name__)

def handle_errors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except PlayerNotFoundError as pnfe:
            logger.error(f"PlayerNotFoundError: {pnfe}")
            return jsonify({'error': str(pnfe)}), HTTPStatus.NOT_FOUND
        except ValueError as ve:
            logger.error(f"ValueError: {ve}")
            return jsonify({'error': str(ve)}), HTTPStatus.BAD_REQUEST
        except Exception as e:
            logger.exception("Unhandled exception occurred")
            return jsonify({'error': 'Internal server error'}), HTTPStatus.INTERNAL_SERVER_ERROR
    return decorated_function