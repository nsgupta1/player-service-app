from flask import Flask
from database.init_db import initialize_database
from routes import players_bp, chat_bp
import logging

def create_app():
    logging.basicConfig(level=logging.INFO)
    app = Flask(__name__)

    # Initialize the database
    initialize_database()

    # Register Blueprints
    app.register_blueprint(players_bp)
    app.register_blueprint(chat_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8000, debug=True)