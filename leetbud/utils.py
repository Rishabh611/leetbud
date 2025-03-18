import sys
import time
import itertools
import re

def loading_animation(stop_event):
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if stop_event.is_set():
            break
        sys.stdout.write('\rAssistant is thinking ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\r')


def draw_box(text, width=80):
    horizontal = "─"
    vertical = "│"
    top_left = "╭"
    top_right = "╮"
    bottom_left = "╰"
    bottom_right = "╯"
    
    # Draw top border
    box = f"{top_left}{horizontal * (width-2)}{top_right}\n"
    
    # Split text into lines and wrap long lines
    lines = []
    for line in text.split('\n'):
        while len(line) > width-4:  # -4 for padding
            split_at = line[:width-4].rfind(' ')
            if split_at == -1:
                split_at = width-4
            lines.append(line[:split_at])
            line = line[split_at:].lstrip()
        lines.append(line)
    
    # Draw content
    for line in lines:
        padding = width - 4 - len(line.replace('\033[91m', '').replace('\033[96m', '').replace('\033[0m', ''))
        box += f"{vertical} {line}{' ' * padding} {vertical}\n"
    
    # Draw bottom border
    box += f"{bottom_left}{horizontal * (width-2)}{bottom_right}"
    return box

def format_response(response):
    # Format bold text
    response = re.sub(r'\*\*(.*?)\*\*', r'\033[1m\033[91m\1\033[0m', response)
    # Format code blocks
    response = re.sub(r'`(.*?)`', r'\033[96m\1\033[0m', response)
    # Format lists
    response = re.sub(r'^- ', r'• ', response, flags=re.MULTILINE)
    # Draw box around the formatted response
    response = draw_box(response)
    
    return response