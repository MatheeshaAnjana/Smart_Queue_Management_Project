

class SkippedStack:

    
    def __init__(self):
        
        # Python list used as stack
        # append() adds to end, pop() removes from end
        self.stack = []
    
    def push(self, token):
        
        # Add token to the top of the stack
        self.stack.append(token)
    
    def pop(self):
       
        if self.is_empty():
            return None
        # Remove and return the top element
        return self.stack.pop()
    
    def peek(self):
       
        if self.is_empty():
            return None
        # Return the last element without removing
        return self.stack[-1]
    
    def is_empty(self):
       
        return len(self.stack) == 0
    
    def size(self):
        
        return len(self.stack)
    
    def get_all(self):
      
        return self.stack.copy()
    
    def clear(self):
       
        self.stack.clear()
    
    def contains(self, token_id):
        
        return any(token['token_id'] == token_id for token in self.stack)
