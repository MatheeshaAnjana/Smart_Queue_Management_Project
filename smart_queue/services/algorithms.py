
from config import Config

class Algorithms:
    
    
    @staticmethod
    def merge_sort(arr, key_func):
        
        # Base case: array of size 0 or 1 is already sorted
        if len(arr) <= 1:
            return arr
        
        # Divide: split array into two halves
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]
        
        # Conquer: recursively sort both halves
        left_sorted = Algorithms.merge_sort(left_half, key_func)
        right_sorted = Algorithms.merge_sort(right_half, key_func)
        
        # Combine: merge the sorted halves
        return Algorithms._merge(left_sorted, right_sorted, key_func)
    
    @staticmethod
    def _merge(left, right, key_func):
       
        result = []
        i = j = 0
        
        # Merge elements in sorted order
        while i < len(left) and j < len(right):
            if key_func(left[i]) <= key_func(right[j]):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        # Append remaining elements
        result.extend(left[i:])
        result.extend(right[j:])
        
        return result
    
    @staticmethod
    def predict_waiting_time(queue_position, avg_service_time=None):
       
        if avg_service_time is None:
            avg_service_time = Config.AVERAGE_SERVICE_TIME
        
        # Position 1 means next to serve (0 wait), position 2 means 1 person ahead
        users_ahead = max(0, queue_position - 1)
        waiting_time = users_ahead * avg_service_time
        
        return waiting_time
    
    @staticmethod
    def load_balance(counters_load, department):
      
        # Get counters for this department
        dept_counters = Config.COUNTERS.get(department, [])
        
        if not dept_counters:
            return None
        
        # Find counter with minimum load
        min_counter = dept_counters[0]
        min_load = counters_load.get(min_counter, 0)
        
        for counter in dept_counters[1:]:
            load = counters_load.get(counter, 0)
            if load < min_load:
                min_load = load
                min_counter = counter
        
        return min_counter
    
    @staticmethod
    def calculate_statistics(ratings_list):
       
        if not ratings_list:
            return {
                'mean': 0,
                'median': 0,
                'mode': 0,
                'total': 0,
                'distribution': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
            }
        
        # Calculate mean
        mean = sum(ratings_list) / len(ratings_list)
        
        # Calculate median
        sorted_ratings = sorted(ratings_list)
        n = len(sorted_ratings)
        if n % 2 == 0:
            median = (sorted_ratings[n//2 - 1] + sorted_ratings[n//2]) / 2
        else:
            median = sorted_ratings[n//2]
        
        # Calculate mode (most frequent rating)
        frequency = {}
        for rating in ratings_list:
            frequency[rating] = frequency.get(rating, 0) + 1
        mode = max(frequency, key=frequency.get)
        
        # Calculate distribution
        distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for rating in ratings_list:
            if 1 <= rating <= 5:
                distribution[rating] += 1
        
        return {
            'mean': round(mean, 2),
            'median': round(median, 2),
            'mode': mode,
            'total': len(ratings_list),
            'distribution': distribution
        }
    
    @staticmethod
    def filter_tokens(tokens, filters):
       
        result = tokens
        
        # Filter by department
        if 'department' in filters and filters['department']:
            result = [t for t in result if t['department'] == filters['department']]
        
        # Filter by user type
        if 'user_type' in filters and filters['user_type']:
            result = [t for t in result if t['user_type'] == filters['user_type']]
        
        # Filter by status
        if 'status' in filters and filters['status']:
            result = [t for t in result if t['status'] == filters['status']]
        
        # Filter by counter
        if 'counter' in filters and filters['counter']:
            result = [t for t in result if t.get('counter') == filters['counter']]
        
        return result
    
    @staticmethod
    def sort_tokens(tokens, sort_by='token_id', reverse=False):
        
        # Define key functions for different sort types
        key_functions = {
            'token_id': lambda t: t['token_id'],
            'priority': lambda t: Config.PRIORITY_LEVELS.get(t['user_type'], 999),
            'waiting_time': lambda t: t.get('waiting_time', 0),
            'timestamp': lambda t: t['timestamp'],
            'department': lambda t: t['department']
        }
        
        key_func = key_functions.get(sort_by, key_functions['token_id'])
        sorted_tokens = Algorithms.merge_sort(tokens, key_func)
        
        if reverse:
            sorted_tokens.reverse()
        
        return sorted_tokens
