"""
Priority Queue Implementation using Manual Min-Heap
This implements a priority-based queue where Emergency > Staff > Student

Data Structure: Min-Heap (Priority Queue)
Time Complexity:
- push(): O(log n)
- pop(): O(log n)
- peek(): O(1)
"""

from datetime import datetime

class PriorityHeap:
    """
    Priority Queue implementation using manually implemented min-heap
    Lower priority numbers are served first (min-heap)
    Priority: Emergency(1) > Staff(2) > Student(3)
    """
    
    def __init__(self, capacity=100):
        """
        Initialize an empty priority queue
        
        Args:
            capacity: Initial maximum capacity of the heap
        """
        self.capacity = capacity
        # Store heap elements as tuples: (priority, counter, token)
        self.heap = [None] * capacity
        self.size_count = 0  # Current number of elements
        self.counter = 0  # Counter to ensure FIFO for same priority
    
    def push(self, token, priority):
        """
        Add a token to the priority queue
        Time Complexity: O(log n)
        
        Args:
            token: Dictionary containing token information
            priority: Integer priority level (1=highest, 3=lowest)
        """
        # Resize if heap is full
        if self.size_count >= self.capacity:
            self._resize()
        
        # Create heap element: (priority, counter, token)
        element = (priority, self.counter, token)
        self.counter += 1
        
        # Insert at the end
        self.heap[self.size_count] = element
        self.size_count += 1
        
        # Bubble up to maintain heap property
        self._bubble_up(self.size_count - 1)
    
    def pop(self):
        """
        Remove and return the highest priority token
        Time Complexity: O(log n)
        
        Returns:
            Token dictionary or None if heap is empty
        """
        if self.is_empty():
            return None
        
        # Get the root element (minimum)
        min_element = self.heap[0]
        
        # Move last element to root
        self.size_count -= 1
        if self.size_count > 0:
            self.heap[0] = self.heap[self.size_count]
            self.heap[self.size_count] = None
            
            # Bubble down to maintain heap property
            self._bubble_down(0)
        else:
            self.heap[0] = None
        
        # Return only the token (third element of tuple)
        return min_element[2]
    
    def peek(self):
        """
        View the highest priority token without removing it
        Time Complexity: O(1)
        
        Returns:
            Token dictionary or None if heap is empty
        """
        if self.is_empty():
            return None
        # Return the token from the root element
        return self.heap[0][2]
    
    def is_empty(self):
        """
        Check if the priority queue is empty
        Time Complexity: O(1)
        
        Returns:
            Boolean indicating if heap is empty
        """
        return self.size_count == 0
    
    def size(self):
        """
        Get the number of tokens in the priority queue
        Time Complexity: O(1)
        
        Returns:
            Integer count of tokens
        """
        return self.size_count
    
    def get_all(self):
        """
        Get all tokens in priority order (for display purposes)
        Time Complexity: O(n log n)
        
        Returns:
            List of all tokens sorted by priority
        """
        # Create a copy of heap elements
        elements = []
        for i in range(self.size_count):
            elements.append(self.heap[i])
        
        # Sort by priority and counter
        elements.sort(key=lambda x: (x[0], x[1]))
        
        # Extract only tokens
        return [token for priority, counter, token in elements]
    
    def clear(self):
        """
        Remove all tokens from the priority queue
        Time Complexity: O(1)
        """
        self.heap = [None] * self.capacity
        self.size_count = 0
        self.counter = 0
    
    def _bubble_up(self, index):
        """
        Bubble up element at index to maintain min-heap property
        Time Complexity: O(log n)
        
        Args:
            index: Index of element to bubble up
        """
        while index > 0:
            parent_index = (index - 1) // 2
            
            # Compare with parent
            if self._compare(self.heap[index], self.heap[parent_index]) < 0:
                # Swap with parent
                self.heap[index], self.heap[parent_index] = \
                    self.heap[parent_index], self.heap[index]
                index = parent_index
            else:
                break
    
    def _bubble_down(self, index):
        """
        Bubble down element at index to maintain min-heap property
        Time Complexity: O(log n)
        
        Args:
            index: Index of element to bubble down
        """
        while True:
            left_child = 2 * index + 1
            right_child = 2 * index + 2
            smallest = index
            
            # Compare with left child
            if (left_child < self.size_count and 
                self._compare(self.heap[left_child], self.heap[smallest]) < 0):
                smallest = left_child
            
            # Compare with right child
            if (right_child < self.size_count and 
                self._compare(self.heap[right_child], self.heap[smallest]) < 0):
                smallest = right_child
            
            # If smallest is not current index, swap and continue
            if smallest != index:
                self.heap[index], self.heap[smallest] = \
                    self.heap[smallest], self.heap[index]
                index = smallest
            else:
                break
    
    def _compare(self, elem1, elem2):
        """
        Compare two heap elements
        Returns: negative if elem1 < elem2, 0 if equal, positive if elem1 > elem2
        
        Args:
            elem1: First element tuple (priority, counter, token)
            elem2: Second element tuple (priority, counter, token)
        """
        # Compare by priority first
        if elem1[0] != elem2[0]:
            return elem1[0] - elem2[0]
        # If same priority, compare by counter (FIFO)
        return elem1[1] - elem2[1]
    
    def _resize(self):
        """
        Double the capacity when heap is full
        Time Complexity: O(n)
        """
        new_capacity = self.capacity * 2
        new_heap = [None] * new_capacity
        
        # Copy existing elements
        for i in range(self.size_count):
            new_heap[i] = self.heap[i]
        
        self.heap = new_heap
        self.capacity = new_capacity