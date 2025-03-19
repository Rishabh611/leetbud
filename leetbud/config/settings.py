"""
Configuration settings for LeetBud application.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# LLM Settings
DEFAULT_MODEL = "gpt-4"
MAX_TOKENS = 1500
MAX_CONVERSATION_HISTORY = 10

# UI Settings
TERMINAL_WIDTH = 80
LOADING_ANIMATION_CHARS = ['|', '/', '-', '\\']
LOADING_ANIMATION_DELAY = 0.1

# Color Settings
COLORS = {
    'USER': '\033[94m',     # Blue
    'ASSISTANT': '\033[92m', # Green
    'CODE': '\033[96m',     # Cyan
    'IMPORTANT': '\033[91m', # Red
    'RESET': '\033[0m'      # Reset
}

# Box Drawing Characters
BOX_CHARS = {
    'horizontal': '─',
    'vertical': '│',
    'top_left': '╭',
    'top_right': '╮',
    'bottom_left': '╰',
    'bottom_right': '╯'
} 