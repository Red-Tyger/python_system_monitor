#working file to build ascii graphing functions for Python System Monitor project
import psutil
import asciichartpy
import random

def clear_screen():
    """Clears the screen using ANSI escape sequences"""
    print('\x1b[2J\x1b[H', end="")
