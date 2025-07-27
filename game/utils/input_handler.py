"""
Cross-platform Input Handler

This module provides cross-platform real-time keyboard input handling
without requiring the Enter key, demonstrating encapsulation and
platform abstraction.
"""

import sys
import threading
import time
from typing import Optional

class InputHandler:
    """
    Cross-platform input handler for real-time keyboard input
    
    Demonstrates:
    - Encapsulation: Platform-specific code hidden behind clean interface
    - Abstraction: Common interface for different platforms
    - Resource Management: Proper setup/cleanup of terminal modes
    """
    
    def __init__(self):
        self._raw_mode_enabled = False
        self._key_buffer = []
        self._buffer_lock = threading.Lock()
        self._input_thread = None
        self._stop_input = False
        
        # Platform detection
        self._is_windows = sys.platform.startswith('win')
        self._is_unix = not self._is_windows
        
        # Platform-specific imports
        if self._is_windows:
            try:
                import msvcrt
                self._msvcrt = msvcrt
            except ImportError:
                print("Warning: msvcrt not available on this platform")
                self._msvcrt = None
        else:
            try:
                import termios
                import tty
                import select
                self._termios = termios
                self._tty = tty
                self._select = select
                self._old_settings = None
            except ImportError:
                print("Warning: termios not available on this platform")
                self._termios = None
    
    def enable_raw_mode(self) -> bool:
        """
        Enable raw mode for immediate key detection
        
        Returns:
            True if successful
        """
        if self._raw_mode_enabled:
            return True
        
        try:
            if self._is_windows:
                self._enable_raw_mode_windows()
            else:
                self._enable_raw_mode_unix()
            
            self._raw_mode_enabled = True
            self._start_input_thread()
            return True
            
        except Exception as e:
            print(f"Failed to enable raw mode: {e}")
            return False
    
    def disable_raw_mode(self) -> bool:
        """
        Disable raw mode and restore normal terminal behavior
        
        Returns:
            True if successful
        """
        if not self._raw_mode_enabled:
            return True
        
        try:
            self._stop_input_thread()
            
            if self._is_windows:
                self._disable_raw_mode_windows()
            else:
                self._disable_raw_mode_unix()
            
            self._raw_mode_enabled = False
            return True
            
        except Exception as e:
            print(f"Failed to disable raw mode: {e}")
            return False
    
    def get_key(self) -> Optional[str]:
        """
        Get the next available key press (non-blocking)
        
        Returns:
            Key name string or None if no key pressed
        """
        with self._buffer_lock:
            if self._key_buffer:
                return self._key_buffer.pop(0)
        return None
    
    def is_key_available(self) -> bool:
        """
        Check if any key is available in the buffer
        
        Returns:
            True if key is available
        """
        with self._buffer_lock:
            return len(self._key_buffer) > 0
    
    def clear_buffer(self) -> None:
        """Clear the key buffer"""
        with self._buffer_lock:
            self._key_buffer.clear()
    
    # Platform-specific implementations
    def _enable_raw_mode_windows(self) -> None:
        """Enable raw mode on Windows"""
        # Windows console is already in a suitable mode for our needs
        pass
    
    def _disable_raw_mode_windows(self) -> None:
        """Disable raw mode on Windows"""
        # No special cleanup needed on Windows
        pass
    
    def _enable_raw_mode_unix(self) -> None:
        """Enable raw mode on Unix/Linux/macOS"""
        if self._termios:
            self._old_settings = self._termios.tcgetattr(sys.stdin.fileno())
            self._tty.setraw(sys.stdin.fileno())
    
    def _disable_raw_mode_unix(self) -> None:
        """Disable raw mode on Unix/Linux/macOS"""
        if self._termios and self._old_settings:
            self._termios.tcsetattr(sys.stdin.fileno(), 
                                   self._termios.TCSADRAIN, 
                                   self._old_settings)
    
    # Input thread management
    def _start_input_thread(self) -> None:
        """Start background thread for input monitoring"""
        if self._input_thread and self._input_thread.is_alive():
            return
        
        self._stop_input = False
        self._input_thread = threading.Thread(target=self._input_worker, daemon=True)
        self._input_thread.start()
    
    def _stop_input_thread(self) -> None:
        """Stop background input thread"""
        self._stop_input = True
        if self._input_thread and self._input_thread.is_alive():
            self._input_thread.join(timeout=1.0)
    
    def _input_worker(self) -> None:
        """Background worker for monitoring input"""
        while not self._stop_input:
            try:
                key = self._get_raw_key()
                if key:
                    normalized_key = self._normalize_key(key)
                    if normalized_key:
                        with self._buffer_lock:
                            self._key_buffer.append(normalized_key)
                            # Limit buffer size to prevent memory issues
                            if len(self._key_buffer) > 10:
                                self._key_buffer = self._key_buffer[-10:]
                
                time.sleep(0.01)  # Small delay to prevent excessive CPU usage
                
            except Exception as e:
                # Silently handle input errors to prevent thread crashes
                time.sleep(0.1)
    
    def _get_raw_key(self) -> Optional[str]:
        """Get raw key input (platform-specific)"""
        if self._is_windows:
            return self._get_key_windows()
        else:
            return self._get_key_unix()
    
    def _get_key_windows(self) -> Optional[str]:
        """Get key input on Windows"""
        if not self._msvcrt:
            return None
        
        try:
            if self._msvcrt.kbhit():
                key = self._msvcrt.getch()
                if isinstance(key, bytes):
                    key = key.decode('utf-8', errors='ignore')
                
                # Handle special keys (arrow keys, etc.)
                if ord(key) == 224:  # Special key prefix
                    special_key = self._msvcrt.getch()
                    if isinstance(special_key, bytes):
                        special_key = special_key.decode('utf-8', errors='ignore')
                    return f"special_{ord(special_key)}"
                
                return key
        except Exception:
            pass
        
        return None
    
    def _get_key_unix(self) -> Optional[str]:
        """Get key input on Unix/Linux/macOS"""
        if not self._select:
            return None
        
        try:
            # Check if input is available (non-blocking)
            if self._select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                key = sys.stdin.read(1)
                
                # Handle escape sequences (arrow keys, etc.)
                if ord(key) == 27:  # ESC character
                    # Try to read the rest of the escape sequence
                    if self._select.select([sys.stdin], [], [], 0.1) == ([sys.stdin], [], []):
                        seq = sys.stdin.read(2)
                        if seq == '[A':
                            return 'arrow_up'
                        elif seq == '[B':
                            return 'arrow_down'
                        elif seq == '[C':
                            return 'arrow_right'
                        elif seq == '[D':
                            return 'arrow_left'
                    return 'escape'
                
                return key
        except Exception:
            pass
        
        return None
    
    def _normalize_key(self, key: str) -> Optional[str]:
        """
        Normalize key input to standard key names
        
        Args:
            key: Raw key input
            
        Returns:
            Normalized key name or None
        """
        if not key:
            return None
        
        # Handle special characters
        if len(key) == 1:
            ascii_code = ord(key)
            
            # Space
            if ascii_code == 32:
                return 'space'
            # Escape
            elif ascii_code == 27:
                return 'escape'
            # Enter
            elif ascii_code in [10, 13]:
                return 'enter'
            # Backspace
            elif ascii_code in [8, 127]:
                return 'backspace'
            # Tab
            elif ascii_code == 9:
                return 'tab'
            # Regular characters
            elif 32 <= ascii_code <= 126:
                return key.lower()
        
        # Handle special key sequences
        elif key.startswith('special_'):
            try:
                code = int(key.split('_')[1])
                # Windows arrow keys
                if code == 72:
                    return 'up'
                elif code == 80:
                    return 'down'
                elif code == 75:
                    return 'left'
                elif code == 77:
                    return 'right'
            except (ValueError, IndexError):
                pass
        
        # Handle Unix arrow keys
        elif key.startswith('arrow_'):
            direction = key.split('_')[1]
            return direction
        
        # Handle other special cases
        elif key == 'escape':
            return 'escape'
        
        return None
    
    def __enter__(self):
        """Context manager entry"""
        self.enable_raw_mode()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disable_raw_mode()

# Example usage:
if __name__ == "__main__":
    print("Testing Input Handler - Press keys (ESC to quit):")
    
    with InputHandler() as input_handler:
        while True:
            key = input_handler.get_key()
            if key:
                print(f"Key pressed: {key}")
                if key == 'escape':
                    break
            time.sleep(0.05)
    
    print("Input testing complete!")
