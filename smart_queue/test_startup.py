#!/usr/bin/env python3
"""
Quick startup test to verify the system works before running
"""

import sys
import os

print("Testing Smart Campus Queue Management System...")
print("=" * 60)

try:
    # Test imports
    print("1. Testing imports...")
    from services.queue_service import queue_service
    from services.algorithms import Algorithms
    from config import Config
    print("   ✓ Core modules imported")
    
    # Test token generation
    print("\n2. Testing token generation...")
    result = queue_service.request_token("Test User", "Student", "Finance")
    if result['success']:
        print(f"   ✓ Token {result['token_id']} generated successfully")
    else:
        raise Exception("Token generation failed")
    
    # Test Flask app
    print("\n3. Testing Flask application...")
    from app import app
    routes_count = len(list(app.url_map.iter_rules()))
    print(f"   ✓ Flask app loaded with {routes_count} routes")
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED! System is ready.")
    print("=" * 60)
    print("\nStarting server on http://localhost:3000")
    print("Press CTRL+C to quit\n")
    
    # Run the app
    app.run(host='0.0.0.0', port=3000, debug=True)
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
