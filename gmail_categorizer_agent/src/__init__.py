"""
Gmail Email Categorization Agent

An intelligent email management system built using the Strands Agents framework.
Automatically categorizes emails into predefined labels and provides periodic summaries.
"""

__version__ = "0.1.0"
__author__ = "Gmail Categorizer Agent Team"
__description__ = "AI-powered Gmail email categorization and summarization agent"

# Package imports
from . import agent
from . import categorizer
from . import gmail_client
from . import config
from . import utils

__all__ = [
    "agent",
    "categorizer", 
    "gmail_client",
    "config",
    "utils"
]
