"""
Path utilities for handling asset loading in both development and PyInstaller environments.
This module ensures the game can find its assets whether running from source or as an executable.
"""
import os
import sys

def get_resource_path(relative_path):
    """
    Get the absolute path to a resource file.
    Works both in development and when packaged with PyInstaller.
    
    Args:
        relative_path (str): Relative path to the resource (e.g., "assets/img/player.png")
    
    Returns:
        str: Absolute path to the resource file
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # Running in normal Python environment
        base_path = os.path.abspath(os.path.dirname(__file__))
        # Go up one level from scenes directory to reach project root
        base_path = os.path.dirname(base_path)
    
    return os.path.join(base_path, relative_path)

def get_save_path(filename):
    """
    Get the path for save files (like high scores).
    Uses the executable's directory for packaged apps, project directory for development.
    
    Args:
        filename (str): Name of the save file
    
    Returns:
        str: Absolute path to the save file
    """
    try:
        # Running as PyInstaller executable
        if hasattr(sys, '_MEIPASS'):
            # Use the directory where the executable is located
            exe_dir = os.path.dirname(os.path.abspath(sys.executable))
            return os.path.join(exe_dir, filename)
        else:
            # Running in development - use project directory
            project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            return os.path.join(project_dir, filename)
    except:
        # Fallback: use current working directory
        return os.path.join(os.getcwd(), filename)
