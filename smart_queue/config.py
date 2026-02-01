"""
Configuration file for Smart Campus Queue Management System
Contains all application settings and constants
"""

class Config:
    """Application configuration class"""
    
    # Flask settings
    SECRET_KEY = 'smart-campus-queue-2024'
    DEBUG = True
    
    # Service configuration
    AVERAGE_SERVICE_TIME = 5  # minutes per token
    
    # Department prefixes
    DEPARTMENTS = {
        'Finance': 'FIN',
        'Library': 'LIB',
        'Administration': 'ADM'
    }
    
    # Priority levels (lower number = higher priority)
    PRIORITY_LEVELS = {
        'Emergency': 1,
        'Staff': 2,
        'Student': 3
    }
    
    # Counter configuration
    COUNTERS = {
        'Finance': ['Finance-1', 'Finance-2'],
        'Library': ['Library-1', 'Library-2'],
        'Administration': ['Admin-1', 'Admin-2']
    }
    
    # Status types
    STATUS_WAITING = 'WAITING'
    STATUS_SERVING = 'SERVING'
    STATUS_SERVED = 'SERVED'
    STATUS_SKIPPED = 'SKIPPED'
