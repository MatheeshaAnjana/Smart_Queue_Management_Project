"""
Normal Queue Implementation using Manual Array-Based Approach
This implements a First-Come-First-Served (FCFS) queue

Data Structure: Queue (FIFO)
Time Complexity:
- enqueue(): O(1)
- dequeue(): O(1)
- peek(): O(1)
"""

class NormalQueue:
    """
    Queue implementation for normal (non-priority) tokens
    Uses a manually implemented circular array for efficient O(1) operations
    """
    
    def __init__(self, capacity=100):
        """
        Initialize an empty queue with a fixed capacity
        
        Args:
            capacity: Maximum number of elements the queue can hold
        """
        self.capacity = capacity
        self.queue = [None] * capacity  # Fixed-size array
        self.front = 0  # Points to the front element
        self.rear = -1  # Points to the last element
        self.count = 0  # Current number of elements
    
    def enqueue(self, token):
        """
        Add a token to the end of the queue
        Time Complexity: O(1)
        
        Args:
            token: Dictionary containing token information
        """
        # Check if queue is full
        if self.count >= self.capacity:
            # Dynamically resize the array if needed
            self._resize()
        
        # Move rear pointer in circular manner
        self.rear = (self.rear + 1) % self.capacity
        self.queue[self.rear] = token
        self.count += 1
    
    def dequeue(self):
        """
        Remove and return the token at the front of the queue
        Time Complexity: O(1)
        
        Returns:
            Token dictionary or None if queue is empty
        """
        if self.is_empty():
            return None
        
        # Get the front element
        token = self.queue[self.front]
        self.queue[self.front] = None  # Clear the slot
        
        # Move front pointer in circular manner
        self.front = (self.front + 1) % self.capacity
        self.count -= 1
        
        return token
    
    def peek(self):
        """
        View the token at the front without removing it
        Time Complexity: O(1)
        
        Returns:
            Token dictionary or None if queue is empty
        """
        if self.is_empty():
            return None
        return self.queue[self.front]
    
    def is_empty(self):
        """
        Check if the queue is empty
        Time Complexity: O(1)
        
        Returns:
            Boolean indicating if queue is empty
        """
        return self.count == 0
    
    def size(self):
        """
        Get the number of tokens in the queue
        Time Complexity: O(1)
        
        Returns:
            Integer count of tokens
        """
        return self.count
    
    def get_all(self):
        """
        Get all tokens in the queue (for display purposes)
        Time Complexity: O(n)
        
        Returns:
            List of all tokens in queue order
        """
        if self.is_empty():
            return []
        
        result = []
        index = self.front
        
        # Traverse the circular queue
        for i in range(self.count):
            result.append(self.queue[index])
            index = (index + 1) % self.capacity
        
        return result
    
    def clear(self):
        """
        Remove all tokens from the queue
        Time Complexity: O(1)
        """
        self.queue = [None] * self.capacity
        self.front = 0
        self.rear = -1
        self.count = 0
    
    def _resize(self):
        """
        Double the capacity when the queue is full
        Time Complexity: O(n)
        """
        new_capacity = self.capacity * 2
        new_queue = [None] * new_capacity
        
        # Copy elements in order to the new array
        index = self.front
        for i in range(self.count):
            new_queue[i] = self.queue[index]
            index = (index + 1) % self.capacity
        
        # Update queue properties
        self.queue = new_queue
        self.capacity = new_capacity
        self.front = 0
        self.rear = self.count - 1