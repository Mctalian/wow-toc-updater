#!/usr/bin/env python3
"""
Bundled runner for toc-interface-updater GitHub Action.
This script includes all dependencies and can run standalone.
"""
import sys
import os

# Add bundled dependencies to path
script_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = os.path.join(script_dir, "lib")
if os.path.exists(lib_dir):
    sys.path.insert(0, lib_dir)

# Import and run main
try:
    from toc_interface_updater.cli import main
    
    if __name__ == "__main__":
        main()
except ImportError as e:
    print(f"Error importing toc_interface_updater: {e}")
    print("Make sure the bundle was built correctly.")
    sys.exit(1)
