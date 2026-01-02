"""
Database module for Ppodo application.
Manages SQLite database with tables for tasks, sessions, stats, profile, and badges.
"""
import sqlite3
from datetime import datetime, date
from pathlib import Path
from typing import List, Dict, Tuple, Optional


class Database:
    """SQLite database manager for Ppodo."""

    def __init__(self, db_path: str = "ppodo.db"):
        """Initialize database connection and create tables if needed."""
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self._create_tables()
        self._initialize_badge_definitions()
        self._initialize_user_profile()

    def _create_tables(self):
        """Create all required tables."""
        # Tasks table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP
            )
        """)

        # Focus sessions table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS focus_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER,
                started_at TIMESTAMP NOT NULL,
                ended_at TIMESTAMP,
                duration_minutes INTEGER DEFAULT 25,
                completed BOOLEAN DEFAULT 0,
                FOREIGN KEY (task_id) REFERENCES tasks(id)
            )
        """)

        # Grape stats table (daily statistics)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS grape_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL UNIQUE,
                grapes_earned INTEGER DEFAULT 0,
                bunches_completed INTEGER DEFAULT 0,
                boxes_completed INTEGER DEFAULT 0
            )
        """)

        # User profile table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_profile (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                level INTEGER DEFAULT 1,
                xp INTEGER DEFAULT 0,
                total_grapes INTEGER DEFAULT 0,
                total_bunches INTEGER DEFAULT 0,
                total_boxes INTEGER DEFAULT 0,
                current_bunch_grapes INTEGER DEFAULT 0,
                current_box_bunches INTEGER DEFAULT 0,
                total_focus_minutes INTEGER DEFAULT 0,
                streak_days INTEGER DEFAULT 0,
                last_focus_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Badge definitions table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS badge_definitions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT NOT NULL,
                icon TEXT NOT NULL,
                category TEXT NOT NULL,
                condition_type TEXT NOT NULL,
                condition_value INTEGER NOT NULL
            )
        """)

        # User badges table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_badges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                badge_id INTEGER NOT NULL,
                earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (badge_id) REFERENCES badge_definitions(id)
            )
        """)

        self.conn.commit()

    def _initialize_badge_definitions(self):
        """Initialize 15 badge definitions if they don't exist."""
        badges = [
            # Milestone badges
            ("첫 걸음", "포도알 1개 획득", "🌱", "마일스톤", "grapes", 1),
            ("첫 송이", "포도송이 1개 완성", "🍇", "마일스톤", "bunches", 1),
            ("첫 상자", "포도상자 1개 완성", "📦", "마일스톤", "boxes", 1),

            # Streak badges
            ("일주일 연속", "7일 연속 집중", "🔥", "연속성", "streak", 7),
            ("끈기왕", "50일 연속 집중", "💪", "연속성", "streak", 50),

            # Daily achievement badges
            ("집중왕", "하루 10개 포도알", "⚡", "일간 성과", "daily_grapes", 10),
            ("한 달 마스터", "한 달 중 25일 집중", "👑", "일간 성과", "monthly_days", 25),

            # Collection badges
            ("백전노장", "포도알 100개 획득", "💯", "수집", "grapes", 100),
            ("포도농장", "포도상자 10개 완성", "🏭", "수집", "boxes", 10),
            ("전설", "포도알 1000개 획득", "🏆", "수집", "grapes", 1000),

            # Time-based badges
            ("새벽형 인간", "오전 6-9시 집중", "🌅", "시간대", "morning_sessions", 10),
            ("올빼미족", "밤 10시 이후 집중", "🦉", "시간대", "night_sessions", 10),

            # Level badge
            ("레벨 마스터", "레벨 10 달성", "⭐", "레벨", "level", 10),

            # Task badge
            ("완벽주의자", "할 일 100개 완료", "✅", "태스크", "tasks_completed", 100),

            # Time badge
            ("시간여행자", "총 100시간 집중", "⏰", "시간", "total_hours", 100),
        ]

        for badge in badges:
            try:
                self.cursor.execute("""
                    INSERT OR IGNORE INTO badge_definitions
                    (name, description, icon, category, condition_type, condition_value)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, badge)
            except sqlite3.IntegrityError:
                pass  # Badge already exists

        self.conn.commit()

    def _initialize_user_profile(self):
        """Initialize user profile if it doesn't exist."""
        self.cursor.execute("SELECT COUNT(*) FROM user_profile WHERE id = 1")
        if self.cursor.fetchone()[0] == 0:
            self.cursor.execute("""
                INSERT INTO user_profile (id) VALUES (1)
            """)
            self.conn.commit()

    # ========== Task Management ==========

    def add_task(self, title: str) -> int:
        """Add a new task and return its ID."""
        self.cursor.execute("""
            INSERT INTO tasks (title) VALUES (?)
        """, (title,))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_tasks(self, completed: Optional[bool] = None) -> List[Dict]:
        """Get all tasks, optionally filtered by completion status."""
        if completed is None:
            self.cursor.execute("""
                SELECT * FROM tasks ORDER BY created_at DESC
            """)
        else:
            self.cursor.execute("""
                SELECT * FROM tasks WHERE completed = ? ORDER BY created_at DESC
            """, (completed,))

        return [dict(row) for row in self.cursor.fetchall()]

    def complete_task(self, task_id: int):
        """Mark a task as completed."""
        self.cursor.execute("""
            UPDATE tasks SET completed = 1, completed_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (task_id,))
        self.conn.commit()

    def delete_task(self, task_id: int):
        """Delete a task."""
        self.cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()

    # ========== Focus Session Management ==========

    def start_session(self, task_id: Optional[int] = None, duration: int = 25) -> int:
        """Start a new focus session and return its ID."""
        self.cursor.execute("""
            INSERT INTO focus_sessions (task_id, started_at, duration_minutes)
            VALUES (?, CURRENT_TIMESTAMP, ?)
        """, (task_id, duration))
        self.conn.commit()
        return self.cursor.lastrowid

    def complete_session(self, session_id: int):
        """Mark a session as completed and update stats."""
        self.cursor.execute("""
            UPDATE focus_sessions
            SET completed = 1, ended_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (session_id,))

        # Update user profile and grape stats
        self._add_grape()
        self._update_streak()

        self.conn.commit()

    def get_today_sessions(self) -> List[Dict]:
        """Get all completed sessions for today."""
        today = date.today().isoformat()
        self.cursor.execute("""
            SELECT * FROM focus_sessions
            WHERE DATE(started_at) = ? AND completed = 1
            ORDER BY started_at DESC
        """, (today,))

        return [dict(row) for row in self.cursor.fetchall()]

    # ========== Grape Management ==========

    def _add_grape(self):
        """Add one grape and handle bunch/box completion."""
        profile = self.get_profile()

        # Add grape
        new_grapes = profile['total_grapes'] + 1
        new_bunch_grapes = profile['current_bunch_grapes'] + 1
        new_bunches = profile['total_bunches']
        new_box_bunches = profile['current_box_bunches']
        new_boxes = profile['total_boxes']

        # Check if bunch completed (10 grapes)
        if new_bunch_grapes >= 10:
            new_bunches += 1
            new_box_bunches += 1
            new_bunch_grapes = 0

        # Check if box completed (10 bunches)
        if new_box_bunches >= 10:
            new_boxes += 1
            new_box_bunches = 0

        # Update profile
        self.cursor.execute("""
            UPDATE user_profile SET
                total_grapes = ?,
                total_bunches = ?,
                total_boxes = ?,
                current_bunch_grapes = ?,
                current_box_bunches = ?
            WHERE id = 1
        """, (new_grapes, new_bunches, new_boxes, new_bunch_grapes, new_box_bunches))

        # Update daily stats
        today = date.today().isoformat()
        self.cursor.execute("""
            INSERT INTO grape_stats (date, grapes_earned, bunches_completed, boxes_completed)
            VALUES (?, 1, ?, ?)
            ON CONFLICT(date) DO UPDATE SET
                grapes_earned = grapes_earned + 1,
                bunches_completed = bunches_completed + excluded.bunches_completed,
                boxes_completed = boxes_completed + excluded.boxes_completed
        """, (today, 1 if new_bunch_grapes == 0 else 0, 1 if new_box_bunches == 0 else 0))

        # Add XP (10 XP per grape)
        self._add_xp(10)

    def _add_xp(self, amount: int):
        """Add XP and handle level ups."""
        profile = self.get_profile()
        new_xp = profile['xp'] + amount
        new_level = profile['level']

        # Check for level up
        while True:
            required_xp = int(100 * (1.5 ** (new_level - 1)))
            if new_xp >= required_xp:
                new_xp -= required_xp
                new_level += 1
            else:
                break

        self.cursor.execute("""
            UPDATE user_profile SET xp = ?, level = ? WHERE id = 1
        """, (new_xp, new_level))

    def _update_streak(self):
        """Update streak days."""
        profile = self.get_profile()
        today = date.today()
        last_focus = profile['last_focus_date']

        if last_focus is None:
            # First time
            new_streak = 1
        else:
            last_focus_date = date.fromisoformat(last_focus) if isinstance(last_focus, str) else last_focus
            days_diff = (today - last_focus_date).days

            if days_diff == 0:
                # Same day, keep streak
                new_streak = profile['streak_days']
            elif days_diff == 1:
                # Consecutive day
                new_streak = profile['streak_days'] + 1
            else:
                # Streak broken
                new_streak = 1

        self.cursor.execute("""
            UPDATE user_profile SET streak_days = ?, last_focus_date = ? WHERE id = 1
        """, (new_streak, today.isoformat()))

    # ========== Profile & Stats ==========

    def get_profile(self) -> Dict:
        """Get user profile."""
        self.cursor.execute("SELECT * FROM user_profile WHERE id = 1")
        return dict(self.cursor.fetchone())

    def get_xp_for_next_level(self, level: int) -> int:
        """Calculate XP required for next level."""
        return int(100 * (1.5 ** (level - 1)))

    def get_today_stats(self) -> Dict:
        """Get today's statistics."""
        today = date.today().isoformat()

        # Get today's grape stats
        self.cursor.execute("""
            SELECT * FROM grape_stats WHERE date = ?
        """, (today,))
        row = self.cursor.fetchone()

        if row:
            stats = dict(row)
        else:
            stats = {'grapes_earned': 0, 'bunches_completed': 0, 'boxes_completed': 0}

        # Get completed sessions count
        sessions = self.get_today_sessions()
        stats['sessions_completed'] = len(sessions)

        return stats

    def get_weekly_stats(self) -> List[Tuple[str, int]]:
        """Get weekly focus time statistics (last 7 days)."""
        self.cursor.execute("""
            SELECT DATE(started_at) as day,
                   SUM(duration_minutes) as total_minutes
            FROM focus_sessions
            WHERE completed = 1
              AND started_at >= date('now', '-7 days')
            GROUP BY DATE(started_at)
            ORDER BY day
        """)

        return [(row[0], row[1] or 0) for row in self.cursor.fetchall()]

    def get_task_distribution(self) -> List[Tuple[str, int]]:
        """Get today's task time distribution."""
        today = date.today().isoformat()

        self.cursor.execute("""
            SELECT t.title, SUM(fs.duration_minutes) as total_minutes
            FROM focus_sessions fs
            JOIN tasks t ON fs.task_id = t.id
            WHERE DATE(fs.started_at) = ? AND fs.completed = 1
            GROUP BY t.id, t.title
            ORDER BY total_minutes DESC
        """, (today,))

        return [(row[0], row[1] or 0) for row in self.cursor.fetchall()]

    # ========== Badge Management ==========

    def get_all_badges(self) -> List[Dict]:
        """Get all badge definitions with earned status."""
        self.cursor.execute("""
            SELECT bd.*,
                   CASE WHEN ub.id IS NOT NULL THEN 1 ELSE 0 END as earned,
                   ub.earned_at
            FROM badge_definitions bd
            LEFT JOIN user_badges ub ON bd.id = ub.badge_id
            ORDER BY bd.category, bd.id
        """)

        return [dict(row) for row in self.cursor.fetchall()]

    def check_and_award_badges(self) -> List[Dict]:
        """Check all badge conditions and award new badges."""
        profile = self.get_profile()
        today_stats = self.get_today_stats()
        new_badges = []

        # Get all badges
        all_badges = self.get_all_badges()

        for badge in all_badges:
            if badge['earned']:
                continue  # Already earned

            earned = False
            condition_type = badge['condition_type']
            condition_value = badge['condition_value']

            # Check conditions
            if condition_type == 'grapes':
                earned = profile['total_grapes'] >= condition_value
            elif condition_type == 'bunches':
                earned = profile['total_bunches'] >= condition_value
            elif condition_type == 'boxes':
                earned = profile['total_boxes'] >= condition_value
            elif condition_type == 'streak':
                earned = profile['streak_days'] >= condition_value
            elif condition_type == 'daily_grapes':
                earned = today_stats['grapes_earned'] >= condition_value
            elif condition_type == 'level':
                earned = profile['level'] >= condition_value
            elif condition_type == 'tasks_completed':
                self.cursor.execute("SELECT COUNT(*) FROM tasks WHERE completed = 1")
                count = self.cursor.fetchone()[0]
                earned = count >= condition_value
            elif condition_type == 'total_hours':
                total_hours = profile.get('total_focus_minutes', 0) / 60
                earned = total_hours >= condition_value

            if earned:
                self.cursor.execute("""
                    INSERT INTO user_badges (badge_id) VALUES (?)
                """, (badge['id'],))
                new_badges.append(badge)

        if new_badges:
            self.conn.commit()

        return new_badges

    def close(self):
        """Close database connection."""
        self.conn.close()
