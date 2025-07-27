"""
Observer Pattern Implementation for Game Events

This module demonstrates the Observer Pattern, which allows objects to be
notified of changes in other objects without tight coupling.

DESIGN PATTERN JUSTIFICATION:
The Observer Pattern is ideal for this T-Rex Runner game because:

1. **Event-Driven Architecture**: The game generates many events (score changes,
   collisions, level ups) that multiple components need to react to.

2. **Loose Coupling**: Game engine doesn't need to know about specific UI
   components, sound systems, or achievement trackers - they register as observers.

3. **Extensibility**: New observers can be added easily without modifying
   existing code (e.g., adding sound effects, particle effects, analytics).

4. **Separation of Concerns**: Core game logic is separated from presentation
   and side effects, making the code more maintainable.

5. **Real-time Updates**: Multiple UI elements can update simultaneously when
   game state changes (score display, speed indicator, etc.).
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List
import weakref
from datetime import datetime

class Observer(ABC):
    """
    Abstract Observer interface
    
    All observers must implement the on_notify method to receive
    notifications about game events.
    """
    
    @abstractmethod
    def on_notify(self, event: str, data: Any = None) -> None:
        """
        Handle notification of an event
        
        Args:
            event: String identifier for the event type
            data: Optional data associated with the event
        """
        pass

class Subject:
    """
    Subject class that manages observers
    
    This is a mixin class that can be inherited by any class that
    needs to notify observers of events.
    """
    
    def __init__(self):
        # Use weak references to prevent memory leaks
        self._observers: List[weakref.ReferenceType] = []
    
    def add_observer(self, observer: Observer) -> None:
        """
        Add an observer to receive notifications
        
        Args:
            observer: Observer instance to add
        """
        # Check if observer is already registered
        for obs_ref in self._observers:
            if obs_ref() is observer:
                return
        
        self._observers.append(weakref.ref(observer))
    
    def remove_observer(self, observer: Observer) -> None:
        """
        Remove an observer from notifications
        
        Args:
            observer: Observer instance to remove
        """
        self._observers = [obs_ref for obs_ref in self._observers 
                          if obs_ref() is not observer and obs_ref() is not None]
    
    def notify_observers(self, event: str, data: Any = None) -> None:
        """
        Notify all observers of an event
        
        Args:
            event: Event type identifier
            data: Optional event data
        """
        # Clean up dead references and notify live observers
        live_observers = []
        for obs_ref in self._observers:
            observer = obs_ref()
            if observer is not None:
                live_observers.append(obs_ref)
                try:
                    observer.on_notify(event, data)
                except Exception as e:
                    print(f"Observer notification error: {e}")
        
        self._observers = live_observers

class ScoreObserver(Observer):
    """
    Observer for score-related events
    
    Demonstrates a concrete observer that tracks and displays score information.
    This observer handles:
    - Score updates and display
    - High score tracking
    - Achievement notifications based on score milestones
    """
    
    def __init__(self):
        self._current_score = 0
        self._high_score = 0
        self._last_milestone = 0
        self._score_history: List[int] = []
        self._achievements: List[str] = []
        
        # Load high score
        self._load_high_score()
    
    @property
    def current_score(self) -> int:
        """Get current score"""
        return self._current_score
    
    @property
    def high_score(self) -> int:
        """Get high score"""
        return self._high_score
    
    @property
    def achievements(self) -> List[str]:
        """Get list of achievements"""
        return self._achievements.copy()
    
    def on_notify(self, event: str, data: Any = None) -> None:
        """
        Handle score-related events
        
        Args:
            event: Event type
            data: Event data
        """
        if event == "score_changed":
            self._handle_score_change(data)
        elif event == "game_start":
            self._handle_game_start()
        elif event == "game_over":
            self._handle_game_over()
        elif event == "difficulty_increased":
            self._handle_difficulty_increase(data)
    
    def _handle_score_change(self, new_score: int) -> None:
        """Handle score change event"""
        old_score = self._current_score
        self._current_score = new_score
        
        # Check for new high score
        if new_score > self._high_score:
            self._high_score = new_score
            self._save_high_score()
        
        # Check for score milestones
        self._check_score_milestones(old_score, new_score)
        
        # Add to score history
        self._score_history.append(new_score)
    
    def _handle_game_start(self) -> None:
        """Handle game start event"""
        self._current_score = 0
        self._last_milestone = 0
        self._score_history.clear()
        print("🎮 New game started! Good luck!")
    
    def _handle_game_over(self) -> None:
        """Handle game over event"""
        print(f"\n🏁 Game Over!")
        print(f"📊 Final Score: {self._current_score}")
        print(f"🏆 High Score: {self._high_score}")
        
        if self._current_score == self._high_score and self._current_score > 0:
            print("🎉 NEW HIGH SCORE! Congratulations!")
            self._achievements.append(f"New High Score: {self._current_score}")
    
    def _handle_difficulty_increase(self, level: int) -> None:
        """Handle difficulty increase event"""
        achievement = f"Reached Level {level}"
        if achievement not in self._achievements:
            self._achievements.append(achievement)
            print(f"🎯 {achievement}!")
    
    def _check_score_milestones(self, old_score: int, new_score: int) -> None:
        """Check if player reached any score milestones"""
        milestones = [50, 100, 250, 500, 1000, 2500, 5000]
        
        for milestone in milestones:
            if old_score < milestone <= new_score:
                achievement = f"Score Milestone: {milestone}"
                if achievement not in self._achievements:
                    self._achievements.append(achievement)
                    print(f"🌟 Milestone reached: {milestone} points!")
    
    def _load_high_score(self) -> None:
        """Load high score from file"""
        try:
            with open("high_score.txt", "r") as f:
                self._high_score = int(f.read().strip())
        except (FileNotFoundError, ValueError):
            self._high_score = 0
    
    def _save_high_score(self) -> None:
        """Save high score to file"""
        try:
            with open("high_score.txt", "w") as f:
                f.write(str(self._high_score))
        except Exception as e:
            print(f"Failed to save high score: {e}")

class GameEventObserver(Observer):
    """
    Observer for general game events
    
    Demonstrates another concrete observer that handles various game events
    like state changes, player actions, and system events.
    """
    
    def __init__(self):
        self._game_started = False
        self._game_paused = False
        self._events_log: List[Dict[str, Any]] = []
        self._session_start_time = None
    
    @property
    def events_log(self) -> List[Dict[str, Any]]:
        """Get events log"""
        return self._events_log.copy()
    
    @property
    def session_duration(self) -> float:
        """Get current session duration in seconds"""
        if self._session_start_time:
            return (datetime.now() - self._session_start_time).total_seconds()
        return 0.0
    
    def on_notify(self, event: str, data: Any = None) -> None:
        """
        Handle game events
        
        Args:
            event: Event type
            data: Event data
        """
        # Log all events
        self._log_event(event, data)
        
        # Handle specific events
        if event == "game_start":
            self._handle_game_start()
        elif event == "game_over":
            self._handle_game_over()
        elif event == "game_paused":
            self._handle_game_paused()
        elif event == "game_resumed":
            self._handle_game_resumed()
        elif event == "obstacle_spawned":
            self._handle_obstacle_spawned(data)
        elif event == "difficulty_increased":
            self._handle_difficulty_increased(data)
    
    def _log_event(self, event: str, data: Any) -> None:
        """Log an event with timestamp"""
        event_entry = {
            "timestamp": datetime.now(),
            "event": event,
            "data": data
        }
        self._events_log.append(event_entry)
        
        # Keep only last 100 events to prevent memory issues
        if len(self._events_log) > 100:
            self._events_log = self._events_log[-100:]
    
    def _handle_game_start(self) -> None:
        """Handle game start event"""
        self._game_started = True
        self._session_start_time = datetime.now()
        print("🚀 T-Rex Runner started!")
        print("🎯 Jump with SPACE, Duck with DOWN, Pause with P")
    
    def _handle_game_over(self) -> None:
        """Handle game over event"""
        self._game_started = False
        duration = self.session_duration
        print(f"⏱️  Session Duration: {duration:.1f} seconds")
        print("🔄 Press SPACE to restart or ESC to quit")
    
    def _handle_game_paused(self) -> None:
        """Handle game pause event"""
        self._game_paused = True
        print("⏸️  Game Paused - Press P to resume")
    
    def _handle_game_resumed(self) -> None:
        """Handle game resume event"""
        self._game_paused = False
        print("▶️  Game Resumed")
    
    def _handle_obstacle_spawned(self, obstacle) -> None:
        """Handle obstacle spawn event"""
        if hasattr(obstacle, 'get_obstacle_type'):
            obstacle_type = obstacle.get_obstacle_type()
            # Could trigger sound effects or visual effects here
    
    def _handle_difficulty_increased(self, level: int) -> None:
        """Handle difficulty increase event"""
        print(f"🔥 Difficulty increased to level {level}!")
        print("💨 Game speed increased!")

class PerformanceObserver(Observer):
    """
    Observer for performance monitoring
    
    Demonstrates how observers can be used for non-gameplay features
    like performance monitoring, analytics, or debugging.
    """
    
    def __init__(self):
        self._frame_count = 0
        self._fps_samples = []
        self._last_fps_time = None
        self._performance_log = []
    
    def on_notify(self, event: str, data: Any = None) -> None:
        """
        Handle performance-related events
        
        Args:
            event: Event type
            data: Event data
        """
        current_time = datetime.now()
        
        if event == "frame_rendered":
            self._handle_frame_rendered(current_time)
        elif event == "game_start":
            self._reset_performance_tracking()
        elif event == "game_over":
            self._report_performance()
    
    def _handle_frame_rendered(self, current_time: datetime) -> None:
        """Handle frame render event for FPS calculation"""
        self._frame_count += 1
        
        if self._last_fps_time:
            delta = (current_time - self._last_fps_time).total_seconds()
            if delta > 0:
                fps = 1.0 / delta
                self._fps_samples.append(fps)
                
                # Keep only last 60 samples (about 3 seconds at 20 FPS)
                if len(self._fps_samples) > 60:
                    self._fps_samples = self._fps_samples[-60:]
        
        self._last_fps_time = current_time
    
    def _reset_performance_tracking(self) -> None:
        """Reset performance tracking for new game"""
        self._frame_count = 0
        self._fps_samples.clear()
        self._last_fps_time = None
        self._performance_log.clear()
    
    def _report_performance(self) -> None:
        """Report performance statistics"""
        if self._fps_samples:
            avg_fps = sum(self._fps_samples) / len(self._fps_samples)
            min_fps = min(self._fps_samples)
            max_fps = max(self._fps_samples)
            
            print(f"\n📊 Performance Report:")
            print(f"🎞️  Total Frames: {self._frame_count}")
            print(f"⚡ Average FPS: {avg_fps:.1f}")
            print(f"🐌 Min FPS: {min_fps:.1f}")
            print(f"🚀 Max FPS: {max_fps:.1f}")
    
    @property
    def current_fps(self) -> float:
        """Get current FPS estimate"""
        if len(self._fps_samples) >= 5:
            # Use last 5 samples for current FPS
            recent_samples = self._fps_samples[-5:]
            return sum(recent_samples) / len(recent_samples)
        return 0.0

# Observer Pattern Benefits:
# 1. Loose Coupling: Observers don't need to know about each other
# 2. Dynamic Relationships: Observers can be added/removed at runtime
# 3. Broadcast Communication: One event can notify multiple observers
# 4. Open/Closed Principle: Easy to add new observers without changing existing code
# 5. Separation of Concerns: Different aspects handled by different observers
