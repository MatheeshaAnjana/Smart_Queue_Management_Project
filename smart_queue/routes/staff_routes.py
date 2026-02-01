"""
Staff Routes - API endpoints for staff operations
Handles serve, skip, recall, and queue management
"""

from flask import Blueprint, request, jsonify
from services.queue_service import queue_service

staff_bp = Blueprint('staff', __name__)

@staff_bp.route('/staff/serve', methods=['POST'])
def serve_next():
    """
    API endpoint to serve the next token in queue
    
    Request body:
        {
            "counter": "Finance-1"
        }
    
    Response:
        {
            "success": true,
            "token": {...}
        }
    """
    try:
        data = request.get_json()
        counter = data.get('counter')
        
        if not counter:
            return jsonify({'error': 'Counter name required'}), 400
        
        result = queue_service.serve_next(counter)
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@staff_bp.route('/staff/complete', methods=['POST'])
def complete_service():
    """
    API endpoint to complete service for current token
    
    Request body:
        {
            "counter": "Finance-1"
        }
    
    Response:
        {
            "success": true
        }
    """
    try:
        data = request.get_json()
        counter = data.get('counter')
        
        if not counter:
            return jsonify({'error': 'Counter name required'}), 400
        
        result = queue_service.complete_service(counter)
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@staff_bp.route('/staff/skip', methods=['POST'])
def skip_token():
    """
    API endpoint to skip the current token
    Pushes token to skip stack for later recall
    
    Request body:
        {
            "counter": "Finance-1"
        }
    
    Response:
        {
            "success": true,
            "token_id": "FIN-001"
        }
    """
    try:
        data = request.get_json()
        counter = data.get('counter')
        
        if not counter:
            return jsonify({'error': 'Counter name required'}), 400
        
        result = queue_service.skip_token(counter)
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@staff_bp.route('/staff/recall', methods=['POST'])
def recall_token():
    """
    API endpoint to recall a skipped token
    Pops token from skip stack and reinserts into priority queue
    
    Request body:
        {
            "department": "Finance"
        }
    
    Response:
        {
            "success": true,
            "token": {...}
        }
    """
    try:
        data = request.get_json()
        department = data.get('department')
        
        if not department:
            return jsonify({'error': 'Department name required'}), 400
        
        result = queue_service.recall_token(department)
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@staff_bp.route('/staff/counter/<counter>', methods=['GET'])
def get_counter_status(counter):
    """
    API endpoint to get status of a specific counter
    
    Response:
        {
            "counter": "Finance-1",
            "current_token": {...},
            "status": "serving",
            "served_count": 10
        }
    """
    try:
        if counter not in queue_service.counter_status:
            return jsonify({'error': 'Invalid counter'}), 404
        
        status = queue_service.counter_status[counter]
        current_token = None
        
        if status['current_token']:
            current_token = queue_service.token_registry.lookup(status['current_token'])
        
        return jsonify({
            'counter': counter,
            'current_token': current_token,
            'status': status['status'],
            'served_count': status['served_count']
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@staff_bp.route('/staff/queue/sorted', methods=['GET'])
def get_sorted_queue():
    """
    API endpoint to get sorted and filtered queue view
    
    Query params:
        department: Department name (required)
        sort_by: Sort criteria (token_id, priority, waiting_time, timestamp)
        status: Filter by status
        user_type: Filter by user type
    
    Response:
        {
            "tokens": [...]
        }
    """
    try:
        department = request.args.get('department')
        sort_by = request.args.get('sort_by', 'token_id')
        
        if not department:
            return jsonify({'error': 'Department required'}), 400
        
        # Build filters
        filters = {}
        if request.args.get('status'):
            filters['status'] = request.args.get('status')
        if request.args.get('user_type'):
            filters['user_type'] = request.args.get('user_type')
        
        # Get sorted queue
        tokens = queue_service.get_sorted_queue(department, sort_by, filters)
        
        return jsonify({'tokens': tokens}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@staff_bp.route('/staff/skipped/<department>', methods=['GET'])
def get_skipped_tokens(department):
    """
    API endpoint to get all skipped tokens for a department
    
    Response:
        {
            "skipped": [...]
        }
    """
    try:
        if department not in queue_service.skipped_stacks:
            return jsonify({'error': 'Invalid department'}), 404
        
        skipped = queue_service.skipped_stacks[department].get_all()
        
        return jsonify({'skipped': skipped}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
