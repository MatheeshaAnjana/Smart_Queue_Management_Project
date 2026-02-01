"""
Stack Implementation for Skipped Tokens
This implements a Last-In-First-Out (LIFO) stack for recall functionality

Data Structure: Stack (LIFO)
Time Complexity:
- push(): O(1)
- pop(): O(1)
- peek(): O(1)
"""

class SkippedStack:
    """
    Stack implementation for managing skipped tokens
    Uses Python list for efficient O(1) operations at the end
    Supports recall functionality (most recently skipped is recalled first)
    """
    
    def __init__(self):
        """Initialize an empty stack"""
        # Python list used as stack
        # append() adds to end, pop() removes from end
        self.stack = []
    
    def push(self, token):
        """
        Push a skipped token onto the stack
        Time Complexity: O(1)
        
        Args:
            token: Dictionary containing token information
        """
        # Add token to the top of the stack
        self.stack.append(token)
    
    def pop(self):
        """
        Pop the most recently skipped token from the stack
        Time Complexity: O(1)
        
        Returns:
            Token dictionary or None if stack is empty
        """
        if self.is_empty():
            return None
        # Remove and return the top element
        return self.stack.pop()
    
    def peek(self):
        """
        View the top token without removing it
        Time Complexity: O(1)
        
        Returns:
            Token dictionary or None if stack is empty
        """
        if self.is_empty():
            return None
        # Return the last element without removing
        return self.stack[-1]
    
    def is_empty(self):
        """
        Check if the stack is empty
        Time Complexity: O(1)
        
        Returns:
            Boolean indicating if stack is empty
        """
        return len(self.stack) == 0
    
    def size(self):
        """
        Get the number of tokens in the stack
        Time Complexity: O(1)
        
        Returns:
            Integer count of tokens
        """
        return len(self.stack)
    
    def get_all(self):
        """
        Get all skipped tokens (for display purposes)
        Time Complexity: O(n)
        
        Returns:
            List of all tokens in stack order (bottom to top)
        """
        return self.stack.copy()
    
    def clear(self):
        """
        Remove all tokens from the stack
        Time Complexity: O(1)
        """
        self.stack.clear()
    
    def contains(self, token_id):
        """
        Check if a specific token is in the stack
        Time Complexity: O(n)
        
        Args:
            token_id: String token identifier
            
        Returns:
            Boolean indicating if token is in stack
        """
        return any(token['token_id'] == token_id for token in self.stack)
