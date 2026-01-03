"""
Internationalization (I18N) system for Ppodo application.
Supports Korean, English, and Japanese.
"""
from typing import Dict, Any


class LanguageManager:
    """Manages application language and translations."""

    SUPPORTED_LANGUAGES = {
        'ko': '한국어',
        'en': 'English',
        'ja': '日本語'
    }

    # Complete translation dictionary
    TRANSLATIONS = {
        'ko': {
            # Application
            'app_title': '🍇 Ppodo (뽀도) - 포도알 뽀모도로 타이머',
            'app_name': 'Ppodo',

            # Timer states
            'state_idle': '⏸ 대기 중',
            'state_focus': '🔥 집중 중',
            'state_break': '☕ 휴식 중',
            'state_paused': '⏸ 일시정지',

            # Buttons
            'btn_start': '▶ 시작',
            'btn_pause': '⏸ 일시정지',
            'btn_stop': '⏹ 중지',
            'btn_resume': '▶ 재개',
            'btn_save': '💾 저장',
            'btn_cancel': '❌ 취소',
            'btn_add': '➕ 추가',
            'btn_delete': '🗑️ 삭제',
            'btn_complete': '✅ 완료',
            'btn_settings': '⚙️ 설정',
            'btn_toggle_tabs': '📑 탭 숨기기/보이기',
            'btn_mini_mode': '🔲 미니 모드',
            'btn_restore': '⬜',
            'btn_close': '✕',

            # Tabs
            'tab_timer': '⏱️ 타이머',
            'tab_tasks': '📝 할 일',
            'tab_stats': '📊 통계',
            'tab_grapes': '🍇 포도',
            'tab_level': '⭐ 레벨',
            'tab_badges': '🏆 뱃지',

            # Grape widget
            'grape_title': '🍇 포도 수확량',
            'grape_total': '전체 수확량',
            'grape_berry': '🟣 포도알',
            'grape_bunch': '🍇 포도송이',
            'grape_box': '📦 포도상자',
            'grape_today': '⭐ 오늘',
            'grape_current_bunch': '현재 송이 진행도',
            'grape_current_box': '현재 상자 진행도',
            'grape_count': '{count}개',
            'grape_bunch_count': '{count}송이',
            'grape_box_count': '{count}상자',

            # Level widget
            'level_title': '⭐ 레벨 & 경험치',
            'level_current': '현재 레벨',
            'level_xp': '경험치',
            'level_stats': '통계',
            'level_total_focus': '총 집중 시간',
            'level_streak': '연속 집중',
            'level_hours': '{hours}시간',
            'level_days': '{days}일',

            # Task widget
            'task_title': '📝 할 일 목록',
            'task_add_placeholder': '새 할 일을 입력하세요...',
            'task_empty': '할 일이 없습니다',
            'task_completed': '완료: {count}개',
            'task_current': '📝 {title}',

            # Stats widget
            'stats_title': '📊 통계 분석',
            'stats_weekly': '주간 집중 시간',
            'stats_task_dist': '오늘 태스크 분포',
            'stats_today': '오늘',
            'stats_total': '전체',
            'stats_focus_time': '집중 시간',
            'stats_sessions': '세션',
            'stats_grapes': '포도알',
            'stats_minutes': '{mins}분',
            'stats_count': '{count}개',
            'stats_session_count': '{count}회',

            # Badge widget
            'badge_title': '🏆 뱃지 컬렉션',
            'badge_unlocked': '획득: {count}/{total}',
            'badge_locked': '🔒 미획득',

            # Settings dialog
            'settings_title': '⚙️ 설정',
            'settings_timer': '⏱️ 타이머 설정',
            'settings_focus_time': '집중 시간:',
            'settings_break_time': '휴식 시간:',
            'settings_minutes': ' 분',
            'settings_language': '🌐 언어 설정',
            'settings_language_label': '언어:',
            'settings_info': '💡 타이머가 실행 중이 아닐 때만 설정을 변경할 수 있습니다.',
            'settings_cannot_change': '설정 불가',
            'settings_timer_running': '타이머가 실행 중일 때는 설정을 변경할 수 없습니다.\n먼저 타이머를 중지해주세요.',

            # Mini window
            'mini_tooltip_restore': '전체 화면으로 돌아가기',
            'mini_tooltip_close': '닫기',

            # Messages
            'msg_focus_complete': '🎉 집중 완료!',
            'msg_focus_done': '🔥 {duration}분 집중 완료!',
            'msg_grape_earned': '🍇 포도알 +1 획득!',
            'msg_xp_earned': '💫 경험치 +10 XP',
            'msg_level_up': '🎉 레벨업! Level {level} 달성!',
            'msg_badge_earned': '🏆 새 뱃지 획득!',
            'msg_break_time': '이제 {mins}분 휴식하세요.',
            'msg_no_grape_warning': '⚠️ 포도알 수집 불가',
            'msg_no_grape_short': '⚠️ 15분 미만 집중이라 포도알을 획득하지 못했습니다.\n다음부터는 15분 이상 집중하여 포도알을 모아보세요!',
            'msg_no_grape_detail': '현재 집중 시간이 {duration}분으로 설정되어 있습니다.\n\n🍇 포도알은 15분 이상 집중했을 때만 모을 수 있습니다.\n\n15분 미만으로 진행하면 포도알을 획득할 수 없습니다.\n그래도 진행하시겠습니까?',
            'msg_break_complete': '☕ 휴식 완료',
            'msg_break_done': '휴식이 끝났습니다.\n다시 집중할 준비가 되셨나요?'
        },

        'en': {
            # Application
            'app_title': '🍇 Podo - Grape Pomodoro Timer',
            'app_name': 'Podo',

            # Timer states
            'state_idle': '⏸ Idle',
            'state_focus': '🔥 Focusing',
            'state_break': '☕ Break',
            'state_paused': '⏸ Paused',

            # Buttons
            'btn_start': '▶ Start',
            'btn_pause': '⏸ Pause',
            'btn_stop': '⏹ Stop',
            'btn_resume': '▶ Resume',
            'btn_save': '💾 Save',
            'btn_cancel': '❌ Cancel',
            'btn_add': '➕ Add',
            'btn_delete': '🗑️ Delete',
            'btn_complete': '✅ Complete',
            'btn_settings': '⚙️ Settings',
            'btn_toggle_tabs': '📑 Toggle Tabs',
            'btn_mini_mode': '🔲 Mini Mode',
            'btn_restore': '⬜',
            'btn_close': '✕',

            # Tabs
            'tab_timer': '⏱️ Timer',
            'tab_tasks': '📝 Tasks',
            'tab_stats': '📊 Statistics',
            'tab_grapes': '🍇 Grapes',
            'tab_level': '⭐ Level',
            'tab_badges': '🏆 Badges',

            # Grape widget
            'grape_title': '🍇 Grape Harvest',
            'grape_total': 'Total Harvest',
            'grape_berry': '🟣 Grapes',
            'grape_bunch': '🍇 Bunches',
            'grape_box': '📦 Boxes',
            'grape_today': '⭐ Today',
            'grape_current_bunch': 'Current Bunch Progress',
            'grape_current_box': 'Current Box Progress',
            'grape_count': '{count}',
            'grape_bunch_count': '{count}',
            'grape_box_count': '{count}',

            # Level widget
            'level_title': '⭐ Level & Experience',
            'level_current': 'Current Level',
            'level_xp': 'Experience',
            'level_stats': 'Statistics',
            'level_total_focus': 'Total Focus Time',
            'level_streak': 'Focus Streak',
            'level_hours': '{hours}h',
            'level_days': '{days}d',

            # Task widget
            'task_title': '📝 Task List',
            'task_add_placeholder': 'Enter a new task...',
            'task_empty': 'No tasks',
            'task_completed': 'Completed: {count}',
            'task_current': '📝 {title}',

            # Stats widget
            'stats_title': '📊 Statistics',
            'stats_weekly': 'Weekly Focus Time',
            'stats_task_dist': 'Today\'s Task Distribution',
            'stats_today': 'Today',
            'stats_total': 'Total',
            'stats_focus_time': 'Focus Time',
            'stats_sessions': 'Sessions',
            'stats_grapes': 'Grapes',
            'stats_minutes': '{mins}m',
            'stats_count': '{count}',
            'stats_session_count': '{count}',

            # Badge widget
            'badge_title': '🏆 Badge Collection',
            'badge_unlocked': 'Unlocked: {count}/{total}',
            'badge_locked': '🔒 Locked',

            # Settings dialog
            'settings_title': '⚙️ Settings',
            'settings_timer': '⏱️ Timer Settings',
            'settings_focus_time': 'Focus Time:',
            'settings_break_time': 'Break Time:',
            'settings_minutes': ' min',
            'settings_language': '🌐 Language',
            'settings_language_label': 'Language:',
            'settings_info': '💡 Settings can only be changed when the timer is not running.',
            'settings_cannot_change': 'Cannot Change Settings',
            'settings_timer_running': 'Settings cannot be changed while the timer is running.\nPlease stop the timer first.',

            # Mini window
            'mini_tooltip_restore': 'Restore to full window',
            'mini_tooltip_close': 'Close',

            # Messages
            'msg_focus_complete': '🎉 Focus Complete!',
            'msg_focus_done': '🔥 {duration} minutes of focus completed!',
            'msg_grape_earned': '🍇 Grape +1 earned!',
            'msg_xp_earned': '💫 Experience +10 XP',
            'msg_level_up': '🎉 Level Up! Level {level} achieved!',
            'msg_badge_earned': '🏆 New badge earned!',
            'msg_break_time': 'Now take a {mins} minute break.',
            'msg_no_grape_warning': '⚠️ Cannot Collect Grape',
            'msg_no_grape_short': '⚠️ No grape earned for focusing less than 15 minutes.\nNext time, focus for at least 15 minutes to collect grapes!',
            'msg_no_grape_detail': 'Current focus time is set to {duration} minutes.\n\n🍇 Grapes can only be collected for 15+ minute sessions.\n\n You won\'t earn grapes for sessions under 15 minutes.\nContinue anyway?',
            'msg_break_complete': '☕ Break Complete',
            'msg_break_done': 'Break is over.\nReady to focus again?'
        },

        'ja': {
            # Application
            'app_title': '🍇 ポド - ぶどうポモドーロタイマー',
            'app_name': 'ポド',

            # Timer states
            'state_idle': '⏸ 待機中',
            'state_focus': '🔥 集中中',
            'state_break': '☕ 休憩中',
            'state_paused': '⏸ 一時停止',

            # Buttons
            'btn_start': '▶ 開始',
            'btn_pause': '⏸ 一時停止',
            'btn_stop': '⏹ 停止',
            'btn_resume': '▶ 再開',
            'btn_save': '💾 保存',
            'btn_cancel': '❌ キャンセル',
            'btn_add': '➕ 追加',
            'btn_delete': '🗑️ 削除',
            'btn_complete': '✅ 完了',
            'btn_settings': '⚙️ 設定',
            'btn_toggle_tabs': '📑 タブ切替',
            'btn_mini_mode': '🔲 ミニモード',
            'btn_restore': '⬜',
            'btn_close': '✕',

            # Tabs
            'tab_timer': '⏱️ タイマー',
            'tab_tasks': '📝 タスク',
            'tab_stats': '📊統計',
            'tab_grapes': '🍇 ぶどう',
            'tab_level': '⭐ レベル',
            'tab_badges': '🏆 バッジ',

            # Grape widget
            'grape_title': '🍇 ぶどう収穫量',
            'grape_total': '合計収穫量',
            'grape_berry': '🟣 ぶどう粒',
            'grape_bunch': '🍇 ぶどう房',
            'grape_box': '📦 ぶどう箱',
            'grape_today': '⭐ 今日',
            'grape_current_bunch': '現在の房進捗',
            'grape_current_box': '現在の箱進捗',
            'grape_count': '{count}個',
            'grape_bunch_count': '{count}房',
            'grape_box_count': '{count}箱',

            # Level widget
            'level_title': '⭐ レベル＆経験値',
            'level_current': '現在のレベル',
            'level_xp': '経験値',
            'level_stats': '統計',
            'level_total_focus': '総集中時間',
            'level_streak': '連続集中',
            'level_hours': '{hours}時間',
            'level_days': '{days}日',

            # Task widget
            'task_title': '📝 タスクリスト',
            'task_add_placeholder': '新しいタスクを入力...',
            'task_empty': 'タスクなし',
            'task_completed': '完了: {count}個',
            'task_current': '📝 {title}',

            # Stats widget
            'stats_title': '📊 統計分析',
            'stats_weekly': '週間集中時間',
            'stats_task_dist': '今日のタスク分布',
            'stats_today': '今日',
            'stats_total': '合計',
            'stats_focus_time': '集中時間',
            'stats_sessions': 'セッション',
            'stats_grapes': 'ぶどう粒',
            'stats_minutes': '{mins}分',
            'stats_count': '{count}個',
            'stats_session_count': '{count}回',

            # Badge widget
            'badge_title': '🏆 バッジコレクション',
            'badge_unlocked': '獲得: {count}/{total}',
            'badge_locked': '🔒 未獲得',

            # Settings dialog
            'settings_title': '⚙️ 設定',
            'settings_timer': '⏱️ タイマー設定',
            'settings_focus_time': '集中時間:',
            'settings_break_time': '休憩時間:',
            'settings_minutes': ' 分',
            'settings_language': '🌐 言語設定',
            'settings_language_label': '言語:',
            'settings_info': '💡 タイマーが実行中でない場合のみ設定を変更できます。',
            'settings_cannot_change': '設定変更不可',
            'settings_timer_running': 'タイマー実行中は設定を変更できません。\n先にタイマーを停止してください。',

            # Mini window
            'mini_tooltip_restore': 'フル画面に戻る',
            'mini_tooltip_close': '閉じる',

            # Messages
            'msg_focus_complete': '🎉 集中完了！',
            'msg_focus_done': '🔥 {duration}分の集中完了！',
            'msg_grape_earned': '🍇 ぶどう粒 +1 獲得！',
            'msg_xp_earned': '💫 経験値 +10 XP',
            'msg_level_up': '🎉 レベルアップ！ レベル {level} 達成！',
            'msg_badge_earned': '🏆 新しいバッジ獲得！',
            'msg_break_time': '今から{mins}分休憩しましょう。',
            'msg_no_grape_warning': '⚠️ ぶどう粒収集不可',
            'msg_no_grape_short': '⚠️ 15分未満の集中のためぶどう粒を獲得できませんでした。\n次回は15分以上集中してぶどう粒を集めましょう！',
            'msg_no_grape_detail': '現在の集中時間は{duration}分に設定されています。\n\n🍇 ぶどう粒は15分以上集中した場合のみ獲得できます。\n\n15分未満では ぶどう粒を獲得できません。\nそれでも続行しますか？',
            'msg_break_complete': '☕ 休憩完了',
            'msg_break_done': '休憩が終わりました。\nまた集中する準備はできましたか？'
        }
    }

    def __init__(self, default_language: str = 'ko'):
        """
        Initialize language manager.

        Args:
            default_language: Default language code (ko, en, ja)
        """
        self._current_language = default_language if default_language in self.SUPPORTED_LANGUAGES else 'ko'

    def get_current_language(self) -> str:
        """Get current language code."""
        return self._current_language

    def set_language(self, language_code: str):
        """
        Set current language.

        Args:
            language_code: Language code (ko, en, ja)
        """
        if language_code in self.SUPPORTED_LANGUAGES:
            self._current_language = language_code

    def get_language_name(self, language_code: str = None) -> str:
        """
        Get language name.

        Args:
            language_code: Language code, uses current if None

        Returns:
            Language name
        """
        code = language_code or self._current_language
        return self.SUPPORTED_LANGUAGES.get(code, self.SUPPORTED_LANGUAGES['ko'])

    def translate(self, key: str, **kwargs) -> str:
        """
        Get translated string.

        Args:
            key: Translation key
            **kwargs: Format parameters

        Returns:
            Translated string with format parameters applied
        """
        translations = self.TRANSLATIONS.get(self._current_language, self.TRANSLATIONS['ko'])
        text = translations.get(key, key)

        # Apply format parameters if provided
        if kwargs:
            try:
                text = text.format(**kwargs)
            except (KeyError, ValueError):
                pass

        return text

    def t(self, key: str, **kwargs) -> str:
        """Shorthand for translate."""
        return self.translate(key, **kwargs)
