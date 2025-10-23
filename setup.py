"""
Setup Script for AI Assistant
Automated setup for beginners
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}:")
        print(f"   {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible!")
    return True

def main():
    """Main setup function"""
    print("🤖 AI Assistant Setup Script")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("\n💡 Try running: pip install --upgrade pip")
        return
    
    # Check for .env file
    if not os.path.exists(".env"):
        print("\n⚠️  .env file not found!")
        print("📝 Please create a .env file with your Google API key:")
        print("   GOOGLE_API_KEY=your_actual_api_key_here")
        print("\n🔗 Get your API key from: https://makersuite.google.com/app/apikey")
    else:
        print("✅ .env file found!")
    
    print("\n🎉 Setup completed!")
    print("\n📋 Next steps:")
    print("1. Add your Google API key to the .env file")
    print("2. Run: streamlit run app.py")
    print("3. Open your browser to the provided URL")
    
    print("\n💡 Need help? Check the README.md file for detailed instructions!")

if __name__ == "__main__":
    main()
