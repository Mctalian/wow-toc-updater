#!/usr/bin/env python3
"""Runner script for the bundled TOC interface updater."""

import sys
import os

# Add bundled dependencies to path
script_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = os.path.join(script_dir, "lib")
sys.path.insert(0, lib_dir)

# Import and run main
from toc_interface_updater.cli import main

if __name__ == "__main__":
    main()
