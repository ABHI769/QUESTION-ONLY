from flask import Flask, render_template, request, jsonify
from ai_model import game_ai, GameState
import time

app = Flask(__name__,template_folder='templates',static_folder='static')


@app.route('/')
def index():
    """Serve the main game page."""
    return render_template('index.html')


@app.route('/api/validate', methods=['POST'])
def validate_question():
    """Validate a user's question without advancing the game."""
    data = request.json
    question = data.get('question', '').strip()
    
    is_valid, error_msg = game_ai.validate_user_question(question)
    
    return jsonify({
        'valid': is_valid,
        'error': error_msg if not is_valid else None
    })


@app.route('/api/play', methods=['POST'])
def play_turn():
    """Process a user's question and return AI's response."""
    data = request.json
    question = data.get('question', '').strip()
    
    result = game_ai.process_user_input(question)
    
    return jsonify(result)


@app.route('/api/state', methods=['GET'])
def get_state():
    """Get current game state."""
    return jsonify(game_ai.get_game_state())


@app.route('/api/rules', methods=['GET'])
def get_rules():
    """Get game rules."""
    return jsonify({'rules': game_ai.get_rules()})


@app.route('/api/reset', methods=['POST'])
def reset_game():
    """Reset the game to initial state."""
    game_ai.reset_game()
    return jsonify({
        'message': 'Game reset successfully!',
        'state': game_ai.get_game_state()
    })


@app.route('/api/history', methods=['GET'])
def get_history():
    """Get conversation history."""
    history = [
        {
            'text': q.text,
            'is_ai': q.is_ai,
            'timestamp': q.timestamp
        }
        for q in game_ai.questions
    ]
    return jsonify({'history': history})


if __name__ == '__main__':
    print("🎮 Starting Question Only Game Server...")
    print("📍 Server running at http://localhost:5000")
    print("💡 Press Ctrl+C to stop the server")
    app.run(debug=True, host='0.0.0.0', port=5000)
