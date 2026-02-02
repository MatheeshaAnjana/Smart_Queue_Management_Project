
from flask import Blueprint, request, jsonify
from services.queue_service import queue_service

staff_bp = Blueprint('staff', __name__)

@staff_bp.route('/staff/serve', methods=['POST'])
def serve_next():

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
 
    try:
        if department not in queue_service.skipped_stacks:
            return jsonify({'error': 'Invalid department'}), 404
        
        skipped = queue_service.skipped_stacks[department].get_all()
        
        return jsonify({'skipped': skipped}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
