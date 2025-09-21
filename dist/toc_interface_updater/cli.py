"""Command line interface for the TOC interface updater."""

import argparse

from .constants import TocSuffix
from .file_processor import process_files
from .types import GameFlavor, VersionCache

# ANSI escape sequences for colors and formatting
RESET = "\033[0m"
GREEN = "\033[32m"
YELLOW = "\033[33m"


def flavor_type(value):
    """Convert string flavor to GameFlavor enum."""
    # Get the current classic expansion name (lowercase) for CLI usage
    current_classic_name = TocSuffix.CURRENT_CLASSIC.lower()
    
    flavor_map = {
        "retail": GameFlavor.WOW,
        "mainline": GameFlavor.WOW,
        "classic": GameFlavor.WOW_CLASSIC,
        current_classic_name: GameFlavor.WOW_CLASSIC,  # Dynamic current classic
        "classic_era": GameFlavor.WOW_CLASSIC_ERA,
        "vanilla": GameFlavor.WOW_CLASSIC_ERA,
    }
    if value.lower() not in flavor_map:
        raise argparse.ArgumentTypeError(
            f"Invalid flavor: {value}. Allowed values are: {', '.join(flavor_map.keys())}"
        )
    return flavor_map[value.lower()]


def main():
    """Main CLI entry point."""
    # Get the current classic expansion name for help text
    current_classic_name = TocSuffix.CURRENT_CLASSIC.lower()
    
    parser = argparse.ArgumentParser(description="WoW TOC Updater")
    parser.add_argument(
        "-b", "--beta", action="store_true", help="Include beta versions"
    )
    parser.add_argument(
        "-p", "--ptr", action="store_true", help="Include test versions"
    )
    parser.add_argument(
        "-f",
        "--flavor",
        type=flavor_type,
        default=GameFlavor.WOW,
        help=f"Game flavor (retail, mainline, classic, {current_classic_name}, classic_era, vanilla)",
    )
    args = parser.parse_args()

    version_cache: VersionCache = {}
    modified_files = process_files(
        args.flavor.value, args.beta, args.ptr, version_cache
    )

    if modified_files:
        print(f"\n{GREEN}Files modified:")
        for modified_file in modified_files:
            print(f"{GREEN}{modified_file}{RESET}")
    else:
        print(f"\n{YELLOW}No files were modified.{RESET}")


if __name__ == "__main__":
    main()
