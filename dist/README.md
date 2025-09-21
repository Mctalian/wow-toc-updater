# Bundled Distribution

This directory contains a self-contained bundle of the TOC interface updater
with all its dependencies.

## Usage

```bash
python3 run.py [options]
```

## Contents

- `run.py` - Main entry point script
- `toc_interface_updater/` - Source code
- `lib/` - Bundled Python dependencies
- `requirements.txt` - List of bundled dependencies

This bundle is designed to work on GitHub Actions runners without requiring
additional package installation.
