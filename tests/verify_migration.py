#!/usr/bin/env python3
"""
Verification script to check the Flask migration is complete and correct.
This script validates the Flask app structure without actually running it.
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists and print status"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} - NOT FOUND")
        return False

def check_flask_app_structure():
    """Verify Flask app has all required routes"""
    try:
        with open('app.py', 'r') as f:
            content = f.read()
        
        required_routes = [
            '/api/version',
            '/api/vl2vg',
            '/api/vl2svg', 
            '/api/vl2png',
            '/api/vl2pdf',
            '/api/vg2svg',
            '/api/vg2png',
            '/api/vg2pdf'
        ]
        
        print("\n🔍 Checking Flask routes:")
        all_routes_found = True
        for route in required_routes:
            if route in content:
                print(f"✅ Route found: {route}")
            else:
                print(f"❌ Route missing: {route}")
                all_routes_found = False
        
        return all_routes_found
    except Exception as e:
        print(f"❌ Error reading app.py: {e}")
        return False

def check_fonts_directory():
    """Verify fonts directory structure"""
    fonts_dir = Path("fonts")
    if not fonts_dir.exists():
        print("❌ Fonts directory not found")
        return False
    
    expected_font_dirs = ["liberation-mono", "liberation-sans", "liberation-serif"]
    print("\n🔍 Checking fonts:")
    all_fonts_found = True
    
    for font_dir in expected_font_dirs:
        font_path = fonts_dir / font_dir
        if font_path.exists():
            print(f"✅ Font directory found: {font_dir}")
        else:
            print(f"❌ Font directory missing: {font_dir}")
            all_fonts_found = False
    
    return all_fonts_found

def main():
    print("🚀 VL-Convert Service Migration Verification")
    print("=" * 50)
    
    # Check core files
    print("\n📁 Checking core files:")
    files_ok = True
    files_ok &= check_file_exists("app.py", "Flask application")
    files_ok &= check_file_exists("requirements.txt", "Python dependencies")
    files_ok &= check_file_exists("Dockerfile", "Docker configuration")
    files_ok &= check_file_exists("docker-compose.yml", "Docker Compose configuration")
    
    # Check Flask app structure
    routes_ok = check_flask_app_structure()
    
    # Check fonts
    fonts_ok = check_fonts_directory()
    
    print("\n" + "=" * 50)
    print("📋 MIGRATION SUMMARY:")
    
    if files_ok and routes_ok and fonts_ok:
        print("✅ Migration completed successfully!")
        print("\n🚀 Ready to deploy! Run one of:")
        print("   • docker-compose up --build")
        print("   • python3 app.py (if dependencies installed)")
        print("   • gunicorn app:app --bind 0.0.0.0:5000")
        return 0
    else:
        print("❌ Migration has issues that need to be resolved")
        return 1

if __name__ == "__main__":
    sys.exit(main())