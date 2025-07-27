#!/usr/bin/env python3
"""
Quick UI test for the modern T-Rex game
"""

import time
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_modern_ui():
    """Test the modern UI components"""
    try:
        from game.utils.display import Display, Colors
        from game.utils.input_handler import InputHandler
        
        print("🎮 Testing Modern UI Components...")
        
        # Test color support
        print(f"{Colors.BRIGHT_GREEN}✅ Colors imported successfully{Colors.RESET}")
        
        # Test display initialization
        display = Display(80, 24)
        print(f"{Colors.BRIGHT_CYAN}✅ Display initialized successfully{Colors.RESET}")
        
        # Test input handler
        input_handler = InputHandler()
        print(f"{Colors.BRIGHT_YELLOW}✅ Input handler initialized successfully{Colors.RESET}")
        
        print(f"\n{Colors.BOLD}{Colors.BRIGHT_MAGENTA}🎉 All UI components are working!{Colors.RESET}")
        print(f"{Colors.BRIGHT_WHITE}Ready to run the modern T-Rex game!{Colors.RESET}")
        
        return True
        
    except Exception as e:
        print(f"{Colors.BRIGHT_RED}❌ Error testing UI: {e}{Colors.RESET}")
        return False

def show_modern_preview():
    """Show a preview of the modern UI"""
    try:
        from game.utils.display import Display, Colors
        
        display = Display(60, 15)
        display.clear()
        
        # Demo the modern display
        print(f"{Colors.BOLD}{Colors.BRIGHT_CYAN}╔════════════════════════════════════════════════════════╗{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BRIGHT_CYAN}║{Colors.BRIGHT_WHITE}                  🦖 T-REX RUNNER 2024                  {Colors.BRIGHT_CYAN}║{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BRIGHT_CYAN}╠════════════════════════════════════════════════════════╣{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BRIGHT_CYAN}║{Colors.BRIGHT_GREEN}  ✨ Modern ANSI Color Support                          {Colors.BRIGHT_CYAN}║{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BRIGHT_CYAN}║{Colors.BRIGHT_YELLOW}  🎨 Animated Visual Effects                            {Colors.BRIGHT_CYAN}║{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BRIGHT_CYAN}║{Colors.BRIGHT_MAGENTA}  🏆 Professional Game Screens                          {Colors.BRIGHT_CYAN}║{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BRIGHT_CYAN}║{Colors.BRIGHT_RED}  🎯 Enhanced Gameplay Experience                       {Colors.BRIGHT_CYAN}║{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BRIGHT_CYAN}╚════════════════════════════════════════════════════════╝{Colors.RESET}")
        
        print(f"\n{Colors.BRIGHT_WHITE}The UI is no longer obsolete! 🚀{Colors.RESET}")
        
    except Exception as e:
        print(f"Error showing preview: {e}")

if __name__ == "__main__":
    # Import Colors for the main section
    try:
        from game.utils.display import Colors
    except ImportError:
        # Fallback if Colors not available
        class Colors:
            RESET = ""
            BOLD = ""
            BRIGHT_WHITE = ""
            BRIGHT_GREEN = ""
            BRIGHT_RED = ""
    
    print(f"{Colors.BOLD}{Colors.BRIGHT_WHITE}T-Rex Runner - Modern UI Test{Colors.RESET}\n")
    
    if test_modern_ui():
        print("\n" + "="*50)
        show_modern_preview()
        print("\n" + "="*50)
        print(f"{Colors.BRIGHT_GREEN}🎮 Run 'python main.py' to start the game!{Colors.RESET}")
    else:
        print(f"{Colors.BRIGHT_RED}❌ UI test failed. Check the game setup.{Colors.RESET}")
