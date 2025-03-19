"""
UI display functionality for LeetBud.
"""
import sys
import time
import threading
import itertools
import re
from typing import Optional

from leetbud.config.settings import (
    COLORS, BOX_CHARS, TERMINAL_WIDTH,
    LOADING_ANIMATION_CHARS, LOADING_ANIMATION_DELAY
)

class Display:
    @staticmethod
    def clear_line():
        """Clear the current line in terminal."""
        sys.stdout.write("\033[F")  # Move cursor up one line
        sys.stdout.write("\033[K")  # Clear the line

    @staticmethod
    def format_user_message(message: str) -> str:
        """Format user message with appropriate styling."""
        return f"{COLORS['USER']}[You]:{COLORS['RESET']} {message}"

    @staticmethod
    def format_markdown(text: str) -> str:
        """Format markdown-style text with colors and styling."""
        # Format bold text
        text = re.sub(r'\*\*(.*?)\*\*', 
                     f"{COLORS['IMPORTANT']}\\1{COLORS['RESET']}", text)
        # Format code blocks
        text = re.sub(r'`(.*?)`', 
                     f"{COLORS['CODE']}\\1{COLORS['RESET']}", text)
        # Format lists
        text = re.sub(r'^- ', '• ', text, flags=re.MULTILINE)
        return text

    @classmethod
    def draw_box(cls, text: str, width: int = TERMINAL_WIDTH) -> str:
        """Draw a box around the text with proper word wrapping."""
        text = cls.format_markdown(text)
        
        # Draw top border
        box = f"{BOX_CHARS['top_left']}{BOX_CHARS['horizontal'] * (width-2)}{BOX_CHARS['top_right']}\n"
        
        # Split text into lines and wrap long lines
        lines = []
        for line in text.split('\n'):
            while len(cls._strip_ansi(line)) > width-4:  # -4 for padding
                split_at = line[:width-4].rfind(' ')
                if split_at == -1:
                    split_at = width-4
                lines.append(line[:split_at])
                line = line[split_at:].lstrip()
            lines.append(line)
        
        # Draw content
        for line in lines:
            padding = width - 4 - len(cls._strip_ansi(line))
            box += f"{BOX_CHARS['vertical']} {line}{' ' * padding} {BOX_CHARS['vertical']}\n"
        
        # Draw bottom border
        box += f"{BOX_CHARS['bottom_left']}{BOX_CHARS['horizontal'] * (width-2)}{BOX_CHARS['bottom_right']}"
        return box

    @staticmethod
    def _strip_ansi(text: str) -> str:
        """Remove ANSI escape sequences from text."""
        ansi_escape = re.compile(r'\033\[[0-9;]*m')
        return ansi_escape.sub('', text)

class LoadingSpinner:
    def __init__(self, message: str = "Assistant is thinking"):
        self.message = message
        self.stop_event = threading.Event()
        self.thread: Optional[threading.Thread] = None

    def start(self):
        """Start the loading animation in a separate thread."""
        self.thread = threading.Thread(target=self._animate)
        self.thread.start()

    def stop(self):
        """Stop the loading animation."""
        if self.thread:
            self.stop_event.set()
            self.thread.join()
            sys.stdout.write('\r')
            sys.stdout.flush()

    def _animate(self):
        """Animate the loading spinner."""
        for c in itertools.cycle(LOADING_ANIMATION_CHARS):
            if self.stop_event.is_set():
                break
            sys.stdout.write(f'\r{self.message} {c}')
            sys.stdout.flush()
            time.sleep(LOADING_ANIMATION_DELAY) 