"""
Smart Campus Queue Management System
Main Flask Application

This is the entry point for the entire queue management system.
It handles routing, API endpoints, and serves HTML pages.
"""

from flask import Flask, render_template, jsonify, request
from datetime import datetime
import os

# Import routes
from routes.user_routes import user_bp
from routes.staff_routes import staff_bp

# Import the global queue service instance
from services.queue_service import queue_service

app = Flask(__name__)
app.config.from_object('config.Config')

# Register blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(staff_bp, url_prefix='/api')

# Main route - Dashboard
@app.route('/')
@app.route('/dashboard')
def dashboard():
    """Render the main dashboard page"""
    return render_template('dashboard.html')

@app.route('/token-request')
def token_request():
    """Render token request page"""
    return render_template('token.html')

@app.route('/public-display')
def public_display():
    """Render public display page"""
    return render_template('public_display.html')

@app.route('/counter-control')
def counter_control():
    """Render counter control page for staff"""
    return render_template('counter_control.html')

@app.route('/sort-filter')
def sort_filter():
    """Render sort and filter page"""
    return render_template('sort_filter.html')

@app.route('/feedback')
def feedback():
    """Render feedback page"""
    return render_template('ratings.html')

@app.route('/analytics')
def analytics():
    """Render analytics page"""
    return render_template('analytics.html')

@app.route('/algorithm-docs')
def algorithm_docs():
    """Render algorithm documentation page"""
    return render_template('algorithm_docs.html')

# API endpoint to get dashboard statistics
@app.route('/api/dashboard/stats')
def get_dashboard_stats():
    """Get real-time dashboard statistics"""
    stats = queue_service.get_dashboard_stats()
    return jsonify(stats)

# API endpoint to get recent activity
@app.route('/api/dashboard/activity')
def get_recent_activity():
    """Get recent token activity"""
    activity = queue_service.get_recent_activity()
    return jsonify(activity)

if __name__ == '__main__':
    print("=" * 60)
    print("Smart Campus Queue Management System")
    print("=" * 60)
    print("Server starting on http://localhost:3000")
    print("Press CTRL+C to quit")
    print("=" * 60)
    app.run(host='0.0.0.0', port=3000, debug=True)
