#!/usr/bin/env python3
"""
CodeWarrior Arena Launcher
This script starts the Flask server and opens the arena.html page in the browser.
"""

import os
import sys
import subprocess
import webbrowser
import time
import threading

def main():
    print("🚀 CodeWarrior Arena Launcher")
    print("=" * 40)
    print("Starting the arena server...")
    
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    backend_file = os.path.join(script_dir, 'backend3ds.py')
    
    # Check if backend3ds.py exists
    if not os.path.exists(backend_file):
        print(f"❌ Error: backend3ds.py not found at {backend_file}")
        input("Press Enter to exit...")
        return
    
    try:
        # Change to the script directory
        os.chdir(script_dir)
        
        print("📍 Server will be available at: http://localhost:5000")
        print("🌐 Arena page will open automatically")
        print("⚡ Press Ctrl+C to stop the server")
        print("-" * 40)
        
        # Run the backend server
        subprocess.run([sys.executable, 'backend3ds.py'])
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except FileNotFoundError:
        print("❌ Error: Python not found. Make sure Python is installed and in PATH.")
        input("Press Enter to exit...")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()