"""
Normal Queue Implementation using collections.deque
This implements a First-Come-First-Served (FCFS) queue

Data Structure: Queue (FIFO)
Time Complexity:
- enqueue(): O(1)
- dequeue(): O(1)
- peek(): O(1)
"""

from collections import deque

class NormalQueue:
    """
    Queue implementation for normal (non-priority) tokens
    Uses Python's deque for efficient O(1) operations at both ends
    """
    
    def __init__(self):
        """Initialize an empty queue using deque"""
        # deque provides O(1) append and popleft operations
        self.queue = deque()
    
    def enqueue(self, token):
        """
        Add a token to the end of the queue
        Time Complexity: O(1)
        
        Args:
            token: Dictionary containing token information
        """
        self.queue.append(token)
    
    def dequeue(self):
        """
        Remove and return the token at the front of the queue
        Time Complexity: O(1)
        
        Returns:
            Token dictionary or None if queue is empty
        """
        if self.is_empty():
            return None
        return self.queue.popleft()
    
    def peek(self):
        """
        View the token at the front without removing it
        Time Complexity: O(1)
        
        Returns:
            Token dictionary or None if queue is empty
        """
        if self.is_empty():
            return None
        return self.queue[0]
    
    def is_empty(self):
        """
        Check if the queue is empty
        Time Complexity: O(1)
        
        Returns:
            Boolean indicating if queue is empty
        """
        return len(self.queue) == 0
    
    def size(self):
        """
        Get the number of tokens in the queue
        Time Complexity: O(1)
        
        Returns:
            Integer count of tokens
        """
        return len(self.queue)
    
    def get_all(self):
        """
        Get all tokens in the queue (for display purposes)
        Time Complexity: O(n)
        
        Returns:
            List of all tokens in queue order
        """
        return list(self.queue)
    
    def clear(self):
        """
        Remove all tokens from the queue
        Time Complexity: O(1)
        """
        self.queue.clear()
