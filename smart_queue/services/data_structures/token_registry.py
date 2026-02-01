"""
Token Registry Implementation using HashMap (Python dict)
This provides O(1) lookup for tokens by ID

Data Structure: HashMap (Python Dictionary)
Time Complexity:
- insert(): O(1) average
- lookup(): O(1) average
- delete(): O(1) average
"""

from datetime import datetime

class TokenRegistry:
    """
    HashMap implementation for fast token lookup and management
    Uses Python's built-in dictionary for O(1) average-case operations
    Stores all tokens with their complete information
    """
    
    def __init__(self):
        """Initialize an empty token registry"""
        # Dictionary to store tokens: {token_id: token_data}
        self.tokens = {}
        # Counter for generating unique token numbers
        self.counters = {
            'FIN': 0,
            'LIB': 0,
            'ADM': 0
        }
    
    def generate_token_id(self, department_prefix):
        """
        Generate a unique token ID for a department
        Time Complexity: O(1)
        
        Args:
            department_prefix: String prefix (FIN, LIB, ADM)
            
        Returns:
            String token ID (e.g., "FIN-001")
        """
        # Increment counter for this department
        self.counters[department_prefix] += 1
        # Format as prefix-number with leading zeros
        token_number = str(self.counters[department_prefix]).zfill(3)
        return f"{department_prefix}-{token_number}"
    
    def insert(self, token_data):
        """
        Insert a token into the registry
        Time Complexity: O(1) average
        
        Args:
            token_data: Dictionary containing token information
        """
        token_id = token_data['token_id']
        self.tokens[token_id] = token_data
    
    def lookup(self, token_id):
        """
        Look up a token by ID
        Time Complexity: O(1) average
        
        Args:
            token_id: String token identifier
            
        Returns:
            Token data dictionary or None if not found
        """
        return self.tokens.get(token_id)
    
    def update(self, token_id, updates):
        """
        Update token information
        Time Complexity: O(1) average
        
        Args:
            token_id: String token identifier
            updates: Dictionary of fields to update
            
        Returns:
            Boolean indicating success
        """
        if token_id in self.tokens:
            self.tokens[token_id].update(updates)
            return True
        return False
    
    def delete(self, token_id):
        """
        Remove a token from the registry
        Time Complexity: O(1) average
        
        Args:
            token_id: String token identifier
            
        Returns:
            Boolean indicating success
        """
        if token_id in self.tokens:
            del self.tokens[token_id]
            return True
        return False
    
    def get_all(self):
        """
        Get all tokens in the registry
        Time Complexity: O(n)
        
        Returns:
            List of all token dictionaries
        """
        return list(self.tokens.values())
    
    def get_by_department(self, department):
        """
        Get all tokens for a specific department
        Time Complexity: O(n)
        
        Args:
            department: String department name
            
        Returns:
            List of tokens for that department
        """
        return [token for token in self.tokens.values() 
                if token['department'] == department]
    
    def get_by_status(self, status):
        """
        Get all tokens with a specific status
        Time Complexity: O(n)
        
        Args:
            status: String status (WAITING, SERVING, SERVED, SKIPPED)
            
        Returns:
            List of tokens with that status
        """
        return [token for token in self.tokens.values() 
                if token['status'] == status]
    
    def count(self):
        """
        Get total number of tokens
        Time Complexity: O(1)
        
        Returns:
            Integer count of tokens
        """
        return len(self.tokens)
    
    def clear(self):
        """
        Remove all tokens from the registry
        Time Complexity: O(1)
        """
        self.tokens.clear()
        self.counters = {'FIN': 0, 'LIB': 0, 'ADM': 0}
