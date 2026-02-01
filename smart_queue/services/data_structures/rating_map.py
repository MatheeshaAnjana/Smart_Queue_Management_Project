"""
Rating Map Implementation using HashMap (Python dict)
This stores and aggregates ratings for analytics

Data Structure: HashMap (Python Dictionary)
Time Complexity:
- add_rating(): O(1) average
- get_average(): O(n) where n is number of ratings for a department
- get_all(): O(1)
"""

from datetime import datetime

class RatingMap:
    """
    HashMap implementation for storing and analyzing ratings
    Uses nested dictionaries for efficient rating aggregation
    Structure: {department: {rating: count}}
    """
    
    def __init__(self):
        """Initialize empty rating storage"""
        # Store ratings by department
        # Structure: {department_name: [list of rating objects]}
        self.ratings = {}
        
        # Store feedback text separately
        # Structure: {department_name: [list of feedback strings]}
        self.feedback = {}
    
    def add_rating(self, department, rating_value, feedback_text="", user_name="", token_id=""):
        """
        Add a rating for a department
        Time Complexity: O(1) average
        
        Args:
            department: String department name
            rating_value: Integer rating (1-5)
            feedback_text: Optional feedback string
            user_name: Optional user name
            token_id: Optional token ID
        """
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
        """
        Calculate average rating for a department
        Time Complexity: O(n) where n is number of ratings
        
        Args:
            department: String department name
            
        Returns:
            Float average rating or 0 if no ratings
        """
        if department not in self.ratings or not self.ratings[department]:
            return 0.0
        
        # Sum all ratings
        total = sum(r['rating'] for r in self.ratings[department])
        count = len(self.ratings[department])
        
        return round(total / count, 2)
    
    def get_count(self, department):
        """
        Get number of ratings for a department
        Time Complexity: O(1)
        
        Args:
            department: String department name
            
        Returns:
            Integer count of ratings
        """
        if department not in self.ratings:
            return 0
        return len(self.ratings[department])
    
    def get_all_averages(self):
        """
        Get average ratings for all departments
        Time Complexity: O(d*n) where d is departments, n is ratings per dept
        
        Returns:
            Dictionary {department: average_rating}
        """
        averages = {}
        for department in self.ratings:
            averages[department] = self.get_average(department)
        return averages
    
    def get_feedback(self, department):
        """
        Get all feedback for a department
        Time Complexity: O(1)
        
        Args:
            department: String department name
            
        Returns:
            List of feedback objects
        """
        return self.feedback.get(department, [])
    
    def get_all_feedback(self):
        """
        Get all feedback for all departments
        Time Complexity: O(1)
        
        Returns:
            Dictionary {department: [feedback_list]}
        """
        return self.feedback
    
    def get_recent_ratings(self, department, limit=10):
        """
        Get most recent ratings for a department
        Time Complexity: O(n)
        
        Args:
            department: String department name
            limit: Maximum number of ratings to return
            
        Returns:
            List of recent rating objects
        """
        if department not in self.ratings:
            return []
        
        # Return last 'limit' ratings (most recent)
        return self.ratings[department][-limit:]
    
    def get_rating_distribution(self, department):
        """
        Get distribution of ratings (1-5 stars) for a department
        Time Complexity: O(n)
        
        Args:
            department: String department name
            
        Returns:
            Dictionary {star_count: number_of_ratings}
        """
        distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        
        if department in self.ratings:
            for rating_obj in self.ratings[department]:
                rating_val = rating_obj['rating']
                if 1 <= rating_val <= 5:
                    distribution[rating_val] += 1
        
        return distribution
    
    def clear(self):
        """
        Remove all ratings and feedback
        Time Complexity: O(1)
        """
        self.ratings.clear()
        self.feedback.clear()
