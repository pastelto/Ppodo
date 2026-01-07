# 🍇 Ppodo

**Grape-themed Pomodoro Timer** - Pomodoro Timer with Gamification

A productivity tool that combines the Pomodoro Technique with grape harvesting gamification elements.

---

## 📝 Overview

**Ppodo** is a Windows desktop application where you earn grapes with each focus session, complete grape bunches and boxes, brew wine, and feel a sense of achievement through leveling up and collecting badges.

### Core Concept
- 🍇 **Pomodoro + Grape = Ppodo**
- 📈 Visualize focus time as "Grape Harvest & Wine Brewing"
- 🎮 A productivity app that grows like an RPG game

---

## ✨ Key Features

### 🌐 Multi-language Support (I18N)
- **한국어 (Korean)** / **English** / **日本語 (Japanese)** support
- Change language in settings
- All UI elements automatically translated

### 🔥 Pomodoro Timer
- **25 min focus / 5 min break** auto-switch (customizable)
- Start, pause, resume, stop functions
- Automatic notifications on focus completion
- Progress bar and state indicator
- **High DPI display support**

### 🍇 Grape Harvest & Wine Brewing System
```
Grape Berry
  ↓ Collect 10
Grape Bunch
  ↓ Collect 10
Grape Box
  ↓ Collect 10
Wine Bottle
  ↓ Collect 10
Wine Crate
```
- 1 Pomodoro completed = 1 Grape Berry earned
- 4-stage evolution system (Grape Harvest → Wine Brewing)
- All stages visualized in 2x2 grid layout
- Today's grape berry statistics

### 📈 Level & Experience System
- 1 Grape Berry = 10 XP
- Level up formula: `100 × (1.5^(N-1))` XP
- Congratulatory message on level up
- Track consecutive focus days
- Record total focus time

### 🏆 Badge System (15 types)

#### Milestones
- 🌱 **First Step**: Earn 1 grape berry
- 🍇 **First Bunch**: Complete 1 grape bunch
- 📦 **First Box**: Complete 1 grape box
- 🍷 **First Wine**: Complete 1 wine bottle
- 🍾 **Wine Master**: Complete 1 wine crate

#### Consistency
- 🔥 **Week Streak**: 7 consecutive days of focus
- 💪 **Persistent**: 50 consecutive days of focus

#### Daily Achievement
- ⚡ **Focus King**: 10 grapes in a day
- 👑 **Monthly Master**: Focus 25 days in a month

#### Collection
- 💯 **Veteran**: Earn 100 grape berries
- 🏭 **Grape Farm**: Complete 10 grape boxes
- 🏆 **Legend**: Earn 1000 grape berries

#### Time-based
- 🌅 **Early Bird**: Focus between 6-9 AM
- 🦉 **Night Owl**: Focus after 10 PM

#### Level
- ⭐ **Level Master**: Reach level 10

#### Tasks
- ✅ **Perfectionist**: Complete 100 tasks

#### Time
- ⏰ **Time Traveler**: 100 hours total focus

### 📝 Task Management
- Add, complete, delete tasks
- Select task before starting focus
- Completed task statistics
- Task history with timestamps

### 📊 Statistics Analysis
- **Weekly Report**: Last 7 days focus time bar chart
- **Task Distribution**: Today's time per task pie chart
- Daily/total statistics display

### 🎨 Premium Themes (5 types)
- **Nordic**: Nordic calmness and intellectual atmosphere (Steel Blue)
- **Midnight**: Deep night's silence and perfect immersion (Dark Slate)
- **Forest**: Forest's phytoncide-like stability (Deep Green)
- **Lavender**: Inspiring and sensual violet (Vivid Violet)
- **Cafe**: Relaxed and warm focus at the cafe (Coffee Bean Brown)

---

## 🛠️ Tech Stack

- **Language**: Python 3.8+
- **UI Framework**: PySide6 (Qt for Python)
- **Database**: SQLite3
- **Charts**: Matplotlib
- **Packaging**: PyInstaller

---

## 📦 Installation & Running

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Application
```bash
python main.py
```

### 3. Build Executable (.exe)
```bash
pyinstaller --noconsole --onefile --name "Ppodo" main.py
```
Generated file: `dist/Ppodo.exe`

---

## 📁 Project Structure

```
Ppodo/
├── main.py                      # Application entry point
├── requirements.txt             # Dependencies list
├── README.md                    # Project documentation (Korean)
├── README_EN.md                 # Project documentation (English)
├── core/                        # Business logic
│   ├── __init__.py
│   ├── timer.py                # Pomodoro timer logic
│   ├── database.py             # SQLite database management
│   ├── theme.py                # Theme system
│   └── i18n.py                 # Multi-language support system
└── ui/                          # UI layer
    ├── __init__.py
    ├── main_window.py          # Main window
    ├── mini_window.py          # Mini window
    ├── timer_widget.py         # Timer display
    ├── task_widget.py          # Task management
    ├── stats_widget.py         # Statistics charts
    ├── grape_widget.py         # Grape collection system
    ├── level_widget.py         # Level & experience
    ├── badge_widget.py         # Badge collection
    ├── history_widget.py       # Task history
    ├── settings_dialog.py      # Settings dialog
    └── styles/                 # Styling modules
        ├── __init__.py
        └── theme_styles.py     # Theme-based style utilities
```

---

## 🎯 How to Use

### 1. Register Tasks
- Add new tasks in "📝 Tasks" tab
- Select task to work on from the list

### 2. Start Focus
- Click "▶ Start" button
- 25-minute timer starts automatically
- Check progress with progress bar

### 3. Complete Focus
- Automatic notification after 25 minutes
- 🍇 Grape Berry +1 earned
- 💫 Experience +10 XP earned
- 5-minute break starts automatically

### 4. Check Statistics
- View weekly focus time in "📊 Stats" tab
- Check time distribution per task

### 5. Collect Badges
- View badge collection in "🏆 Badges" tab
- Badges automatically awarded when conditions are met

---

## 🎮 Gamification Reward System

### Immediate Rewards
- ✅ Pomodoro completed → Grape Berry +1
- ⭐ Experience +10 XP

### Short-term Goals
- 🍇 10 Grape Berries → Grape Bunch completed
- 🏆 10 grapes in a day → "Focus King" badge

### Mid-term Goals
- 📦 10 Grape Bunches → Grape Box completed
- 🍷 10 Grape Boxes → Wine Bottle completed
- ⭐ Reach Level 5
- 🔥 7 consecutive days → "Week Streak" badge

### Long-term Goals
- 🍾 10 Wine Bottles → Wine Crate completed (Final stage!)
- ⭐ Reach Level 10 → "Level Master" badge
- 🏆 1000 Grape Berries → "Legend" badge
- 🎖️ Collect all 15 badges

---

## 📊 Database Schema

### Main Tables
- **tasks**: Task management
- **focus_sessions**: Focus session records
- **grape_stats**: Daily grape berry statistics
- **user_profile**: User level/experience/statistics
- **badge_definitions**: Badge definitions (15 types)
- **user_badges**: User earned badges

All data is stored in local SQLite database (`ppodo.db`).

---

## 🚀 Future Development Plan

### Phase 2 (Enhanced UX)
- [ ] Grape berry earning animation effects
- [ ] Level up celebration animation
- [ ] Badge acquisition zoom effect
- [ ] Sound effects (earning sound, level up sound)

### Phase 3 (Advanced Features)
- [ ] Monthly statistics and trend analysis
- [ ] Custom notification sounds
- [ ] Data export (CSV/JSON)
- [ ] Seasonal limited badges
- [ ] Challenge system

### Phase 4 (Storage & Cloud Integration)
- [ ] Multiple storage backend support
  - [x] Local SQLite (default)
  - [ ] Notion Database integration
  - [ ] Supabase integration
- [ ] Cloud synchronization
- [ ] Data migration tool
- [ ] Real-time backup feature

### Phase 5 (Social Features)
- [ ] Compare with friends
- [ ] Weekly rankings
- [ ] Share badges

---

## 👤 Developer

**Dahae Julie Kim**

---

## 📄 License

This project is created for personal productivity enhancement.

---

## 🙏 Acknowledgments

Thanks to Francesco Cirillo for creating the Pomodoro Technique.

---

**Version**: 2.2
**Last Updated**: 2026-01-03
**Development Started**: 2025-01-02

**New Features (v2.2)**:
- 🍷 Wine brewing system added (4-stage evolution)
- 📦 Progress visualization with 2x2 grid layout
- 🍇 Grape harvest → Wine bottle → Wine crate completion goal

**Previous Update (v2.1)**:
- 🌐 Multi-language support (Korean, English, Japanese)
- 📱 High DPI display optimization
- 🎨 Improved UI visibility

---

Focus, grow, harvest grapes, and brew wine! 🍇🍷✨
