"""
Configuration package for Gmail Email Categorization Agent

Contains system prompts, Gmail label definitions, email templates,
and other configuration constants used throughout the application.
"""

# Configuration imports
from . import prompts
from . import labels  
from . import templates

__all__ = [
    "prompts",
    "labels",
    "templates"
]
