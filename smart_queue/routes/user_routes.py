from flask import Blueprint, request, jsonify
from services.queue_service import queue_service
from services.algorithms import Algorithms

user_bp = Blueprint('user', __name__)

@user_bp.route('/token/request', methods=['POST'])
def request_token():
    """
    API endpoint to request a new token
    
    Request body:
        {
            "user_name": "John Doe",
            "user_type": "Student/Staff/Emergency",
            "department": "Finance/Library/Administration"
        }
    
    Response:
        {
            "success": true,
            "token_id": "FIN-001",
            "queue_position": 3,
            "waiting_time": 10,
            "counter": "Finance-1"
        }
    """
    try:
        data = request.get_json()
        
        user_name = data.get('user_name')
        user_type = data.get('user_type')
        department = data.get('department')
        
        # Validate input
        if not all([user_name, user_type, department]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Request token from service
        result = queue_service.request_token(user_name, user_type, department)
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/queue/status', methods=['GET'])
def get_queue_status():
    """
    API endpoint to get current queue status
    
    Query params:
        department (optional): Filter by department
    
    Response:
        {
            "queues": [...]
        }
    """
    try:
        department = request.args.get('department')
        
        # Get public display data
        display_data = queue_service.get_public_display_data()
        
        # Filter by department if specified
        if department:
            display_data = [d for d in display_data if d['department'] == department]
        
        return jsonify({'queues': display_data}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/token/<token_id>', methods=['GET'])
def get_token_info(token_id):
    """
    API endpoint to get information about a specific token
    
    Response:
        {
            "token_id": "FIN-001",
            "user_name": "John",
            "status": "WAITING",
            ...
        }
    """
    try:
        token = queue_service.token_registry.lookup(token_id)
        
        if not token:
            return jsonify({'error': 'Token not found'}), 404
        
        # Calculate current position and waiting time
        department = token['department']
        position = queue_service._get_queue_position(department, token_id)
        waiting_time = Algorithms.predict_waiting_time(position)
        
        token_info = {
            **token,
            'queue_position': position,
            'waiting_time': waiting_time
        }
        
        return jsonify(token_info), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/rating', methods=['POST'])
def submit_rating():
    """
    API endpoint to submit rating and feedback
    
    Request body:
        {
            "token_id": "FIN-001",
            "rating": 5,
            "feedback": "Great service!"
        }
    
    Response:
        {
            "success": true
        }
    """
    try:
        data = request.get_json()
        
        token_id = data.get('token_id')
        rating = data.get('rating')
        feedback = data.get('feedback', '')
        
        # Validate input
        if not token_id or not rating:
            return jsonify({'error': 'Missing required fields'}), 400
        
        if not (1 <= rating <= 5):
            return jsonify({'error': 'Rating must be between 1 and 5'}), 400
        
        # Submit rating
        result = queue_service.add_rating(token_id, rating, feedback)
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/analytics', methods=['GET'])
def get_analytics():
    """
    API endpoint to get analytics data
    
    Response:
        {
            "analytics": [
                {
                    "department": "Finance",
                    "average_rating": 4.5,
                    "total_ratings": 100,
                    "distribution": {...}
                },
                ...
            ]
        }
    """
    try:
        analytics = queue_service.get_analytics()
        return jsonify({'analytics': analytics}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
