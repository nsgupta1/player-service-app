from flask import Blueprint, jsonify
import ollama

chat_bp = Blueprint('chat_bp', __name__, url_prefix='/v1/chat')

@chat_bp.route('/list-models')
def list_models():
    models = ollama.list()
    # Convert the ListResponse to a list of dictionaries
    serializable_models = [model.model_dump() for model in models.models]
    return jsonify(serializable_models)

@chat_bp.route('', methods=['POST'])
def chat():
    # Process the data as needed
    response = ollama.chat(model='tinyllama', messages=[
        {
            'role': 'user',
            'content': 'Why is the sky blue?',
        },
    ])
    return jsonify(response), 200