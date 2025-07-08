#!/usr/bin/env python3
"""
Launcher script for the SQLite CLI tool
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlcli import main

if __name__ == '__main__':
    main()
