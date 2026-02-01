"""
Priority Queue Implementation using heapq
This implements a priority-based queue where Emergency > Staff > Student

Data Structure: Min-Heap (Priority Queue)
Time Complexity:
- push(): O(log n)
- pop(): O(log n)
- peek(): O(1)
"""

import heapq
from datetime import datetime

class PriorityHeap:
    """
    Priority Queue implementation using Python's heapq module
    Lower priority numbers are served first (min-heap)
    Priority: Emergency(1) > Staff(2) > Student(3)
    """
    
    def __init__(self):
        """Initialize an empty priority queue"""
        # List to store heap elements
        # Each element is a tuple: (priority, timestamp, token)
        self.heap = []
        # Counter to ensure FIFO for same priority
        self.counter = 0
    
    def push(self, token, priority):
        """
        Add a token to the priority queue
        Time Complexity: O(log n)
        
        Args:
            token: Dictionary containing token information
            priority: Integer priority level (1=highest, 3=lowest)
        """
        # Use counter as tiebreaker to maintain FIFO for same priority
        # Heap structure: (priority, counter, token)
        heapq.heappush(self.heap, (priority, self.counter, token))
        self.counter += 1
    
    def pop(self):
        """
        Remove and return the highest priority token
        Time Complexity: O(log n)
        
        Returns:
            Token dictionary or None if heap is empty
        """
        if self.is_empty():
            return None
        # Extract and return only the token (third element)
        priority, counter, token = heapq.heappop(self.heap)
        return token
    
    def peek(self):
        """
        View the highest priority token without removing it
        Time Complexity: O(1)
        
        Returns:
            Token dictionary or None if heap is empty
        """
        if self.is_empty():
            return None
        # Return the token from the first element
        return self.heap[0][2]
    
    def is_empty(self):
        """
        Check if the priority queue is empty
        Time Complexity: O(1)
        
        Returns:
            Boolean indicating if heap is empty
        """
        return len(self.heap) == 0
    
    def size(self):
        """
        Get the number of tokens in the priority queue
        Time Complexity: O(1)
        
        Returns:
            Integer count of tokens
        """
        return len(self.heap)
    
    def get_all(self):
        """
        Get all tokens in priority order (for display purposes)
        Time Complexity: O(n log n)
        
        Returns:
            List of all tokens sorted by priority
        """
        # Return tokens in priority order
        # Extract only the token part from each heap element
        return [token for priority, counter, token in sorted(self.heap)]
    
    def clear(self):
        """
        Remove all tokens from the priority queue
        Time Complexity: O(1)
        """
        self.heap.clear()
        self.counter = 0
