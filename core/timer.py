"""
Timer module for Ppodo application.
Manages Pomodoro timer logic with focus and break cycles.
"""
from enum import Enum
from typing import Callable, Optional
from PySide6.QtCore import QTimer, QObject, Signal


class TimerState(Enum):
    """Timer state enumeration."""
    IDLE = "idle"
    FOCUS = "focus"
    BREAK = "break"
    PAUSED = "paused"


class PomodoroTimer(QObject):
    """Pomodoro timer with focus/break cycles."""

    # Signals
    tick = Signal(int)  # Emitted every second with remaining seconds
    state_changed = Signal(str)  # Emitted when state changes
    focus_completed = Signal()  # Emitted when focus session completes
    break_completed = Signal()  # Emitted when break completes

    def __init__(self, focus_minutes: int = 25, break_minutes: int = 5):
        """
        Initialize Pomodoro timer.

        Args:
            focus_minutes: Duration of focus session in minutes
            break_minutes: Duration of break session in minutes
        """
        super().__init__()

        self.focus_duration = focus_minutes * 60  # Convert to seconds
        self.break_duration = break_minutes * 60  # Convert to seconds

        self.state = TimerState.IDLE
        self.remaining_seconds = 0
        self.total_seconds = 0

        # Qt timer for countdown
        self.qt_timer = QTimer()
        self.qt_timer.timeout.connect(self._on_tick)
        self.qt_timer.setInterval(1000)  # 1 second

    def start_focus(self):
        """Start a focus session."""
        self.state = TimerState.FOCUS
        self.remaining_seconds = self.focus_duration
        self.total_seconds = self.focus_duration
        self.qt_timer.start()
        self.state_changed.emit(self.state.value)
        self.tick.emit(self.remaining_seconds)

    def start_break(self):
        """Start a break session."""
        self.state = TimerState.BREAK
        self.remaining_seconds = self.break_duration
        self.total_seconds = self.break_duration
        self.qt_timer.start()
        self.state_changed.emit(self.state.value)
        self.tick.emit(self.remaining_seconds)

    def pause(self):
        """Pause the current session."""
        if self.state in (TimerState.FOCUS, TimerState.BREAK):
            self.qt_timer.stop()
            self.state = TimerState.PAUSED
            self.state_changed.emit(self.state.value)

    def resume(self):
        """Resume from pause."""
        if self.state == TimerState.PAUSED:
            # Restore previous state based on total_seconds
            if self.total_seconds == self.focus_duration:
                self.state = TimerState.FOCUS
            else:
                self.state = TimerState.BREAK

            self.qt_timer.start()
            self.state_changed.emit(self.state.value)

    def stop(self):
        """Stop and reset the timer."""
        self.qt_timer.stop()
        self.state = TimerState.IDLE
        self.remaining_seconds = 0
        self.total_seconds = 0
        self.state_changed.emit(self.state.value)
        self.tick.emit(self.remaining_seconds)

    def _on_tick(self):
        """Handle timer tick (called every second)."""
        self.remaining_seconds -= 1
        self.tick.emit(self.remaining_seconds)

        if self.remaining_seconds <= 0:
            self._on_complete()

    def _on_complete(self):
        """Handle session completion."""
        self.qt_timer.stop()

        if self.state == TimerState.FOCUS:
            self.focus_completed.emit()
            # Auto-start break
            self.start_break()
        elif self.state == TimerState.BREAK:
            self.break_completed.emit()
            self.state = TimerState.IDLE
            self.state_changed.emit(self.state.value)

    def get_remaining_time(self) -> tuple[int, int]:
        """
        Get remaining time as (minutes, seconds).

        Returns:
            Tuple of (minutes, seconds)
        """
        minutes = self.remaining_seconds // 60
        seconds = self.remaining_seconds % 60
        return (minutes, seconds)

    def get_progress_percent(self) -> float:
        """
        Get progress percentage (0-100).

        Returns:
            Progress as percentage
        """
        if self.total_seconds == 0:
            return 0.0

        elapsed = self.total_seconds - self.remaining_seconds
        return (elapsed / self.total_seconds) * 100

    def set_durations(self, focus_minutes: int, break_minutes: int):
        """
        Update focus and break durations.

        Args:
            focus_minutes: New focus duration in minutes
            break_minutes: New break duration in minutes
        """
        self.focus_duration = focus_minutes * 60
        self.break_duration = break_minutes * 60

    def is_running(self) -> bool:
        """Check if timer is currently running."""
        return self.state in (TimerState.FOCUS, TimerState.BREAK)

    def is_focus(self) -> bool:
        """Check if currently in focus mode."""
        return self.state == TimerState.FOCUS

    def is_break(self) -> bool:
        """Check if currently in break mode."""
        return self.state == TimerState.BREAK

    def is_paused(self) -> bool:
        """Check if timer is paused."""
        return self.state == TimerState.PAUSED

    def is_idle(self) -> bool:
        """Check if timer is idle."""
        return self.state == TimerState.IDLE
