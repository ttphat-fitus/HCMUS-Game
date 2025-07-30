#!/usr/bin/env python3
"""
Setup script for Dino Run Python Game

This script helps users set up the game environment and dependencies.
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error during {description.lower()}: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is adequate"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 6:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} is supported")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} is too old. Please use Python 3.6 or newer.")
        return False

def create_virtual_environment():
    """Create a virtual environment"""
    venv_name = "venv"
    
    if os.path.exists(venv_name):
        print(f"✓ Virtual environment '{venv_name}' already exists")
        return True
    
    return run_command(f"python -m venv {venv_name}", "Creating virtual environment")

def get_activation_command():
    """Get the appropriate activation command for the platform"""
    system = platform.system().lower()
    if system == "windows":
        return "venv\\Scripts\\activate"
    else:
        return "source venv/bin/activate"

def install_requirements():
    """Install required packages"""
    system = platform.system().lower()
    
    if system == "windows":
        pip_command = "venv\\Scripts\\pip install -r requirements.txt"
    else:
        pip_command = "venv/bin/pip install -r requirements.txt"
    
    return run_command(pip_command, "Installing required packages")

def test_pygame():
    """Test if pygame can be imported"""
    print("\nTesting pygame installation...")
    try:
        system = platform.system().lower()
        if system == "windows":
            python_command = "venv\\Scripts\\python -c \"import pygame; print('Pygame version:', pygame.version.ver)\""
        else:
            python_command = "venv/bin/python -c \"import pygame; print('Pygame version:', pygame.version.ver)\""
        
        result = subprocess.run(python_command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ Pygame test successful: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError:
        print("✗ Pygame test failed")
        return False

def main():
    """Main setup function"""
    print("=== Dino Run Python Game Setup ===")
    print("This script will set up the game environment for you.\n")
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Create virtual environment
    if not create_virtual_environment():
        return False
    
    # Install requirements
    if not install_requirements():
        return False
    
    # Test pygame
    if not test_pygame():
        return False
    
    # Success message
    print("\n" + "="*50)
    print("🎮 Setup completed successfully!")
    print("="*50)
    print("\nTo run the game:")
    print("1. Activate the virtual environment:")
    activation_cmd = get_activation_command()
    print(f"   {activation_cmd}")
    print("2. Run the game:")
    print("   python main.py")
    print("\nGame Controls:")
    print("   SPACE - Jump / Start Game")
    print("   DOWN ARROW - Duck")
    print("   ESC - Quit Game")
    print("\nEnjoy the game! 🦕")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Setup failed. Please check the errors above and try again.")
        sys.exit(1)
