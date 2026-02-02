

from datetime import datetime

class TokenRegistry:
   
    
    def __init__(self):
        
        # Dictionary to store tokens: {token_id: token_data}
        self.tokens = {}
        # Counter for generating unique token numbers
        self.counters = {
            'FIN': 0,
            'LIB': 0,
            'ADM': 0
        }
    
    def generate_token_id(self, department_prefix):
       
        # Increment counter for this department
        self.counters[department_prefix] += 1
        # Format as prefix-number with leading zeros
        token_number = str(self.counters[department_prefix]).zfill(3)
        return f"{department_prefix}-{token_number}"
    
    def insert(self, token_data):
       
        token_id = token_data['token_id']
        self.tokens[token_id] = token_data
    
    def lookup(self, token_id):
        
        return self.tokens.get(token_id)
    
    def update(self, token_id, updates):
        
        if token_id in self.tokens:
            self.tokens[token_id].update(updates)
            return True
        return False
    
    def delete(self, token_id):
        
        if token_id in self.tokens:
            del self.tokens[token_id]
            return True
        return False
    
    def get_all(self):
       
        return list(self.tokens.values())
    
    def get_by_department(self, department):
        
        return [token for token in self.tokens.values() 
                if token['department'] == department]
    
    def get_by_status(self, status):
        
        return [token for token in self.tokens.values() 
                if token['status'] == status]
    
    def count(self):
        
        return len(self.tokens)
    
    def clear(self):
        
        self.tokens.clear()
        self.counters = {'FIN': 0, 'LIB': 0, 'ADM': 0}
