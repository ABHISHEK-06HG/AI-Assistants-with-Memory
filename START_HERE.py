#!/usr/bin/env python3
"""
My AI Assistant - Quick Start Script
Run this file to start the AI Assistant
"""

import subprocess
import sys
import os

def main():
    print("🤖 My AI Assistant - Quick Start")
    print("=" * 40)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        print("Please install Python from https://python.org")
        return
    
    # Check if .env exists
    if not os.path.exists(".env"):
        print("⚠️ .env file not found!")
        print("📝 Please create .env file with your API keys")
        print("💡 Copy .env.sample to .env and add your keys")
        return
    
    print("✅ All checks passed!")
    print("🚀 Starting My AI Assistant...")
    
    # Start Streamlit
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Stopping AI Assistant...")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
