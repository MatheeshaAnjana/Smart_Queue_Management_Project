

from datetime import datetime
from config import Config
from services.data_structures.normal_queue import NormalQueue
from services.data_structures.priority_heap import PriorityHeap
from services.data_structures.skipped_stack import SkippedStack
from services.data_structures.token_registry import TokenRegistry
from services.data_structures.rating_map import RatingMap
from services.algorithms import Algorithms

class QueueService:
   
    
    def __init__(self):
        """Initialize all data structures"""
        # Token registry (HashMap) for O(1) lookups
        self.token_registry = TokenRegistry()
        
        # Rating storage (HashMap) for analytics
        self.rating_map = RatingMap()
        
        # Queues for each department
        # Each department has normal queue, priority queue, and skipped stack
        self.queues = {}
        self.skipped_stacks = {}
        
        for dept in Config.DEPARTMENTS.keys():
            self.queues[dept] = {
                'normal': NormalQueue(),
                'priority': PriorityHeap()
            }
            self.skipped_stacks[dept] = SkippedStack()
        
        # Counter status tracking
        self.counter_status = {}
        for dept, counters in Config.COUNTERS.items():
            for counter in counters:
                self.counter_status[counter] = {
                    'current_token': None,
                    'status': 'idle',
                    'served_count': 0
                }
        
        # Statistics
        self.stats = {
            'total_tokens': 0,
            'total_served': 0,
            'total_waiting': 0,
            'total_skipped': 0
        }
    
    def request_token(self, user_name, user_type, department):
        
        # Get department prefix
        dept_prefix = Config.DEPARTMENTS.get(department)
        if not dept_prefix:
            return {'error': 'Invalid department'}
        
        # Generate unique token ID
        token_id = self.token_registry.generate_token_id(dept_prefix)
        
        # Load balance: assign to counter with least load
        counter_loads = self._get_counter_loads(department)
        assigned_counter = Algorithms.load_balance(counter_loads, department)
        
        # Create token data
        token_data = {
            'token_id': token_id,
            'user_name': user_name,
            'user_type': user_type,
            'department': department,
            'counter': assigned_counter,
            'status': Config.STATUS_WAITING,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'priority': Config.PRIORITY_LEVELS.get(user_type, 3)
        }
        
        # Add to token registry
        self.token_registry.insert(token_data)
        
        # Add to appropriate queue based on user type
        if user_type == 'Emergency':
            # High priority - use priority queue
            self.queues[department]['priority'].push(token_data, 1)
        elif user_type == 'Staff':
            # Medium priority - use priority queue
            self.queues[department]['priority'].push(token_data, 2)
        else:
            # Normal priority - use FCFS queue
            self.queues[department]['normal'].enqueue(token_data)
        
        # Update statistics
        self.stats['total_tokens'] += 1
        self.stats['total_waiting'] += 1
        
        # Calculate queue position and waiting time
        queue_position = self._get_queue_position(department, token_id)
        waiting_time = Algorithms.predict_waiting_time(queue_position)
        
        return {
            'success': True,
            'token_id': token_id,
            'queue_position': queue_position,
            'waiting_time': waiting_time,
            'counter': assigned_counter,
            'department': department
        }
    
    def serve_next(self, counter):
        
        # Determine department from counter name
        department = self._get_department_from_counter(counter)
        if not department:
            return {'error': 'Invalid counter'}
        
        # Check priority queue first
        token = self.queues[department]['priority'].pop()
        
        # If no priority tokens, check normal queue
        if token is None:
            token = self.queues[department]['normal'].dequeue()
        
        if token is None:
            return {'error': 'No tokens in queue'}
        
        # Update token status
        token_id = token['token_id']
        self.token_registry.update(token_id, {
            'status': Config.STATUS_SERVING,
            'counter': counter,
            'serve_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
        # Update counter status
        self.counter_status[counter]['current_token'] = token_id
        self.counter_status[counter]['status'] = 'serving'
        
        # Update statistics
        self.stats['total_waiting'] -= 1
        
        return {'success': True, 'token': token}
    
    def complete_service(self, counter):
       
        current_token_id = self.counter_status[counter]['current_token']
        
        if not current_token_id:
            return {'error': 'No active token'}
        
        # Update token status
        self.token_registry.update(current_token_id, {
            'status': Config.STATUS_SERVED,
            'complete_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
        # Update counter status
        self.counter_status[counter]['current_token'] = None
        self.counter_status[counter]['status'] = 'idle'
        self.counter_status[counter]['served_count'] += 1
        
        # Update statistics
        self.stats['total_served'] += 1
        
        return {'success': True}
    
    def skip_token(self, counter):
        
        current_token_id = self.counter_status[counter]['current_token']
        
        if not current_token_id:
            return {'error': 'No active token'}
        
        # Get token data
        token = self.token_registry.lookup(current_token_id)
        department = token['department']
        
        # Update token status
        self.token_registry.update(current_token_id, {
            'status': Config.STATUS_SKIPPED
        })
        
        # Push to skipped stack
        self.skipped_stacks[department].push(token)
        
        # Clear counter
        self.counter_status[counter]['current_token'] = None
        self.counter_status[counter]['status'] = 'idle'
        
        # Update statistics
        self.stats['total_skipped'] += 1
        
        return {'success': True, 'token_id': current_token_id}
    
    def recall_token(self, department):
        
        # Pop from skipped stack
        token = self.skipped_stacks[department].pop()
        
        if token is None:
            return {'error': 'No skipped tokens'}
        
        # Update token status
        token_id = token['token_id']
        self.token_registry.update(token_id, {
            'status': Config.STATUS_WAITING
        })
        
        # Reinsert into priority queue with high priority
        self.queues[department]['priority'].push(token, 1)
        
        # Update statistics
        self.stats['total_skipped'] -= 1
        self.stats['total_waiting'] += 1
        
        return {'success': True, 'token': token}
    
    def get_public_display_data(self):
        
        display_data = []
        
        for dept, counters in Config.COUNTERS.items():
            for counter in counters:
                status = self.counter_status[counter]
                
                # Get current serving token
                current_token = None
                if status['current_token']:
                    current_token = self.token_registry.lookup(status['current_token'])
                
                # Get next token in queue
                next_token = None
                if not self.queues[dept]['priority'].is_empty():
                    next_token = self.queues[dept]['priority'].peek()
                elif not self.queues[dept]['normal'].is_empty():
                    next_token = self.queues[dept]['normal'].peek()
                
                # Calculate waiting time
                queue_length = (self.queues[dept]['priority'].size() + 
                              self.queues[dept]['normal'].size())
                waiting_time = Algorithms.predict_waiting_time(queue_length + 1)
                
                display_data.append({
                    'counter': counter,
                    'department': dept,
                    'current_token': current_token,
                    'next_token': next_token,
                    'queue_length': queue_length,
                    'waiting_time': waiting_time
                })
        
        return display_data
    
    def get_dashboard_stats(self):
        
        # Count currently serving
        serving_count = sum(1 for c in self.counter_status.values() 
                          if c['current_token'] is not None)
        
        # Calculate average waiting time
        total_waiting = self.stats['total_waiting']
        avg_wait = Algorithms.predict_waiting_time(total_waiting // 6 if total_waiting > 0 else 0)
        
        return {
            'pending': self.stats['total_waiting'],
            'serving': serving_count,
            'served': self.stats['total_served'],
            'avg_wait': avg_wait
        }
    
    def get_recent_activity(self, limit=10):
        
        all_tokens = self.token_registry.get_all()
        # Sort by timestamp (most recent first)
        sorted_tokens = sorted(all_tokens, 
                             key=lambda t: t['timestamp'], 
                             reverse=True)
        return sorted_tokens[:limit]
    
    def add_rating(self, token_id, rating, feedback=""):
        
        token = self.token_registry.lookup(token_id)
        if not token:
            return {'error': 'Invalid token'}
        
        department = token['department']
        user_name = token['user_name']
        
        self.rating_map.add_rating(department, rating, feedback, user_name, token_id)
        
        return {'success': True}
    
    def get_analytics(self):
        
        analytics = []
        
        for dept in Config.DEPARTMENTS.keys():
            avg_rating = self.rating_map.get_average(dept)
            rating_count = self.rating_map.get_count(dept)
            distribution = self.rating_map.get_rating_distribution(dept)
            
            analytics.append({
                'department': dept,
                'average_rating': avg_rating,
                'total_ratings': rating_count,
                'distribution': distribution
            })
        
        # Sort by average rating (descending)
        analytics = sorted(analytics, key=lambda x: x['average_rating'], reverse=True)
        
        return analytics
    
    def get_sorted_queue(self, department, sort_by='token_id', filters=None):
        
        # Get all tokens for department
        tokens = self.token_registry.get_by_department(department)
        
        # Apply filters
        if filters:
            tokens = Algorithms.filter_tokens(tokens, filters)
        
        # Sort tokens
        sorted_tokens = Algorithms.sort_tokens(tokens, sort_by)
        
        return sorted_tokens
    
    # Helper methods
    
    def _get_queue_position(self, department, token_id):
        
        position = 1
        
        # Check priority queue
        priority_tokens = self.queues[department]['priority'].get_all()
        for token in priority_tokens:
            if token['token_id'] == token_id:
                return position
            position += 1
        
        # Check normal queue
        normal_tokens = self.queues[department]['normal'].get_all()
        for token in normal_tokens:
            if token['token_id'] == token_id:
                return position
            position += 1
        
        return position
    
    def _get_counter_loads(self, department):
       
        loads = {}
        for counter in Config.COUNTERS.get(department, []):
            # Count tokens assigned to this counter
            tokens = [t for t in self.token_registry.get_all() 
                     if t.get('counter') == counter and t['status'] == Config.STATUS_WAITING]
            loads[counter] = len(tokens)
        return loads
    
    def _get_department_from_counter(self, counter):
        
        for dept, counters in Config.COUNTERS.items():
            if counter in counters:
                return dept
        return None

# Create a global instance
queue_service = QueueService()
