

from datetime import datetime

class RatingMap:
   
    
    def __init__(self):
       
        # Store ratings by department
        # Structure: {department_name: [list of rating objects]}
        self.ratings = {}
        
        # Store feedback text separately
        # Structure: {department_name: [list of feedback strings]}
        self.feedback = {}
    
    def add_rating(self, department, rating_value, feedback_text="", user_name="", token_id=""):
      
        # Initialize department list if not exists
        if department not in self.ratings:
            self.ratings[department] = []
            self.feedback[department] = []
        
        # Create rating object
        rating_obj = {
            'rating': rating_value,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'user_name': user_name,
            'token_id': token_id
        }
        
        # Add to ratings list
        self.ratings[department].append(rating_obj)
        
        # Add feedback if provided
        if feedback_text:
            feedback_obj = {
                'text': feedback_text,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'user_name': user_name,
                'token_id': token_id,
                'rating': rating_value
            }
            self.feedback[department].append(feedback_obj)
    
    def get_average(self, department):
        
        if department not in self.ratings or not self.ratings[department]:
            return 0.0
        
        # Sum all ratings
        total = sum(r['rating'] for r in self.ratings[department])
        count = len(self.ratings[department])
        
        return round(total / count, 2)
    
    def get_count(self, department):
    
        if department not in self.ratings:
            return 0
        return len(self.ratings[department])
    
    def get_all_averages(self):
       
        averages = {}
        for department in self.ratings:
            averages[department] = self.get_average(department)
        return averages
    
    def get_feedback(self, department):
       
        return self.feedback.get(department, [])
    
    def get_all_feedback(self):
      
        return self.feedback
    
    def get_recent_ratings(self, department, limit=10):
        
        if department not in self.ratings:
            return []
        
        # Return last 'limit' ratings (most recent)
        return self.ratings[department][-limit:]
    
    def get_rating_distribution(self, department):
       
        distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        
        if department in self.ratings:
            for rating_obj in self.ratings[department]:
                rating_val = rating_obj['rating']
                if 1 <= rating_val <= 5:
                    distribution[rating_val] += 1
        
        return distribution
    
    def clear(self):
       
        self.ratings.clear()
        self.feedback.clear()
