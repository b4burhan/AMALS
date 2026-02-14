#!/usr/bin/env python
"""
Setup script for Django E-Commerce Platform
Run this script to set up the project automatically.
"""

import os
import sys
import subprocess


def run_command(command, description):
    """Run a shell command and print status"""
    print(f"\n{'='*50}")
    print(f"{description}...")
    print(f"{'='*50}")
    
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"❌ Error: {description} failed")
        return False
    print(f"✅ {description} completed")
    return True


def main():
    """Main setup function"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║           Django E-Commerce Platform Setup                   ║
    ║                                                              ║
    ║  This script will set up the project automatically.         ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Check Python version
    if sys.version_info < (3, 10):
        print("❌ Python 3.10 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python version: {sys.version.split()[0]}")
    
    # Install requirements
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        sys.exit(1)
    
    # Run migrations
    if not run_command("python manage.py migrate", "Running database migrations"):
        sys.exit(1)
    
    # Generate dummy data
    if not run_command("python generate_dummy_data.py", "Generating dummy data"):
        sys.exit(1)
    
    # Collect static files
    if not run_command("python manage.py collectstatic --noinput", "Collecting static files"):
        sys.exit(1)
    
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                    Setup Complete!                           ║
    ║                                                              ║
    ║  You can now run the server with:  
            venv\Scripts\activate                         ║
    ║     python manage.py runserver                              ║
    ║                                                              ║
    ║  Access the application at:                                 ║
    ║     http://127.0.0.1:8000/                                  ║
    ║                                                              ║
    ║  Admin Panel:                                               ║
    ║     http://127.0.0.1:8000/admin/                            ║
    ║     Username: admin                                         ║
    ║     Password: admin123                                      ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)


if __name__ == '__main__':
    main()
