

class NormalQueue:
  
    def __init__(self, capacity=100):
       
        self.capacity = capacity
        self.queue = [None] * capacity  # Fixed-size array
        self.front = 0  # Points to the front element
        self.rear = -1  # Points to the last element
        self.count = 0  # Current number of elements
    
    def enqueue(self, token):
      
        # Check if queue is full
        if self.count >= self.capacity:
            # Dynamically resize the array if needed
            self._resize()
        
        # Move rear pointer in circular manner
        self.rear = (self.rear + 1) % self.capacity
        self.queue[self.rear] = token
        self.count += 1
    
    def dequeue(self):
       
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
       
        if self.is_empty():
            return None
        return self.queue[self.front]
    
    def is_empty(self):
        
        return self.count == 0
    
    def size(self):
       
        return self.count
    
    def get_all(self):
       
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
       
        self.queue = [None] * self.capacity
        self.front = 0
        self.rear = -1
        self.count = 0
    
    def _resize(self):
        
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