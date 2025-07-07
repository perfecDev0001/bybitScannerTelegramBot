#!/usr/bin/env python3
"""
Setup script for Bybit Scanner
Helps with initial configuration and testing
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"🚀 {title}")
    print("="*60)

def check_python_version():
    """Check if Python version is compatible"""
    print_header("CHECKING PYTHON VERSION")
    
    version = sys.version_info
    print(f"Current Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        return False
    
    print("✅ Python version is compatible")
    return True

def create_virtual_environment():
    """Create virtual environment if it doesn't exist"""
    print_header("SETTING UP VIRTUAL ENVIRONMENT")
    
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True
    
    try:
        print("Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Virtual environment created successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False

def install_dependencies():
    """Install required dependencies"""
    print_header("INSTALLING DEPENDENCIES")
    
    # Determine pip path
    if os.name == 'nt':  # Windows
        pip_path = Path("venv/Scripts/pip")
    else:  # Unix/Linux/macOS
        pip_path = Path("venv/bin/pip")
    
    if not pip_path.exists():
        print("❌ Virtual environment not found. Please run setup again.")
        return False
    
    try:
        print("Installing dependencies from requirements.txt...")
        subprocess.run([str(pip_path), "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def check_env_file():
    """Check and help configure .env file"""
    print_header("CHECKING CONFIGURATION")
    
    env_path = Path(".env")
    
    if not env_path.exists():
        print("❌ .env file not found")
        return False
    
    # Read current .env file
    with open(env_path, 'r') as f:
        env_content = f.read()
    
    # Check for placeholder values
    issues = []
    
    if 'TELEGRAM_CHAT_ID=YOUR_CHAT_ID_HERE' in env_content:
        issues.append("TELEGRAM_CHAT_ID needs to be configured")
    
    if 'TELEGRAM_BOT_TOKEN=' in env_content and len(env_content.split('TELEGRAM_BOT_TOKEN=')[1].split('\n')[0]) < 10:
        issues.append("TELEGRAM_BOT_TOKEN appears to be empty or invalid")
    
    if issues:
        print("⚠️  Configuration issues found:")
        for issue in issues:
            print(f"   - {issue}")
        
        print("\n📝 To fix these issues:")
        print("1. Create a Telegram bot with @BotFather")
        print("2. Get your chat ID from @userinfobot")
        print("3. Update the .env file with your actual values")
        
        return False
    
    print("✅ Configuration looks good")
    return True

def run_tests():
    """Run the test suite"""
    print_header("RUNNING TESTS")
    
    # Determine python path
    if os.name == 'nt':  # Windows
        python_path = Path("venv/Scripts/python")
    else:  # Unix/Linux/macOS
        python_path = Path("venv/bin/python")
    
    if not python_path.exists():
        print("❌ Virtual environment not found")
        return False
    
    try:
        print("Running test suite...")
        result = subprocess.run([str(python_path), "test_scanner.py"], 
                              capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("Errors:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("✅ Tests completed")
            return True
        else:
            print("⚠️  Some tests may have failed - check output above")
            return False
            
    except Exception as e:
        print(f"❌ Failed to run tests: {e}")
        return False

def show_next_steps():
    """Show next steps to user"""
    print_header("NEXT STEPS")
    
    print("🎉 Setup completed! Here's what to do next:")
    print()
    print("1. 📱 Configure Telegram (if not done yet):")
    print("   - Create bot with @BotFather")
    print("   - Get chat ID from @userinfobot")
    print("   - Update .env file")
    print()
    print("2. 🧪 Test locally:")
    if os.name == 'nt':  # Windows
        print("   venv\\Scripts\\activate")
    else:  # Unix/Linux/macOS
        print("   source venv/bin/activate")
    print("   python test_scanner.py")
    print()
    print("3. 🚀 Run the scanner:")
    print("   python app.py  (web server + scanner)")
    print("   python scanner.py  (scanner only)")
    print()
    print("4. 🌐 Deploy to Render:")
    print("   - Push to GitHub")
    print("   - Create Render web service")
    print("   - Set environment variables")
    print("   - Deploy!")
    print()
    print("📚 For detailed instructions, see README.md")

def main():
    """Main setup function"""
    print("🚀 BYBIT SCANNER SETUP")
    print("This script will help you set up the Bybit Scanner")
    
    steps = [
        ("Python Version", check_python_version),
        ("Virtual Environment", create_virtual_environment),
        ("Dependencies", install_dependencies),
        ("Configuration", check_env_file),
    ]
    
    success_count = 0
    
    for step_name, step_func in steps:
        try:
            if step_func():
                success_count += 1
            else:
                print(f"\n⚠️  {step_name} step had issues")
        except Exception as e:
            print(f"\n❌ {step_name} step failed: {e}")
    
    print_header("SETUP SUMMARY")
    print(f"Completed: {success_count}/{len(steps)} steps")
    
    if success_count == len(steps):
        print("✅ All setup steps completed successfully!")
        
        # Ask if user wants to run tests
        try:
            response = input("\n🧪 Would you like to run the test suite now? (y/n): ").lower()
            if response in ['y', 'yes']:
                run_tests()
        except KeyboardInterrupt:
            print("\nSkipping tests...")
    else:
        print("⚠️  Some setup steps had issues. Please resolve them before proceeding.")
    
    show_next_steps()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Setup cancelled by user")
    except Exception as e:
        print(f"\n❌ Setup failed with error: {e}")
        print("Please check the error and try again")