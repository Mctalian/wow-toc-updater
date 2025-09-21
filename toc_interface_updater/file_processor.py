"""File processing logic for TOC files."""

import os
import re
from typing import List

from .constants import TocSuffix
from .types import FullProduct, VersionCache

# ANSI escape sequences for colors and formatting
RESET = "\033[0m"
BOLD = "\033[1m"
LIGHT_BLUE = "\033[94m"
GREEN = "\033[32m"
YELLOW = "\033[33m"

line_ending = "\n"


def write_file_if_changed(
    file_path: str,
    original_content: str,
    updated_content: str,
    modified_files: List[str],
) -> None:
    """Write the file only if content has changed, preserving original line endings."""
    if updated_content != original_content:
        # Restore the original line endings before writing back to the file
        updated_content_with_original_line_endings = updated_content.replace(
            "\n", line_ending
        )

        with open(
            file_path, "w", newline=""
        ) as f:  # Ensure the newline='' to allow custom line endings
            f.write(updated_content_with_original_line_endings)

        modified_files.append(file_path)
        print(f"{GREEN}Updated{RESET}")
    else:
        print(f"{YELLOW}No change{RESET}")


def get_product_for_file(
    file_path: str, pattern: re.Pattern, default_flavor: str
) -> tuple[FullProduct, bool]:
    """
    Determine the product and multi-line setting for a file.
    Returns (product, is_multi_line)
    """
    if not pattern.search(file_path):
        # File doesn't match pattern, process with default flavor and multi-line for other products
        return default_flavor, False

    # File matches pattern, determine specific product
    if TocSuffix.MAINLINE in file_path:
        return "wow", False
    elif TocSuffix.CLASSIC in file_path or TocSuffix.CURRENT_CLASSIC in file_path:
        return "wow_classic", False
    elif TocSuffix.VANILLA in file_path:
        return "wow_classic_era", False

    return default_flavor, False


def process_files(
    flavor: str, beta: bool, test: bool, version_cache: VersionCache
) -> List[str]:
    """Process all .toc files in the current directory and subdirectories."""
    from .update import update_versions  # Import here to avoid circular imports

    modified_files: List[str] = []
    pattern = TocSuffix.get_pattern()

    for root, _, files in os.walk("."):
        for file in files:
            if not file.endswith(".toc"):
                continue

            file_path = os.path.join(root, file)

            if not pattern.search(file_path):
                # Process with default flavor and all product types
                update_versions(
                    file_path, flavor, False, beta, test, version_cache, modified_files
                )
                update_versions(
                    file_path,
                    "wow_classic",
                    True,
                    beta,
                    test,
                    version_cache,
                    modified_files,
                )
                update_versions(
                    file_path,
                    "wow_classic_era",
                    True,
                    beta,
                    test,
                    version_cache,
                    modified_files,
                )
            else:
                # Process specific product based on file name
                product, multi = get_product_for_file(file_path, pattern, flavor)
                update_versions(
                    file_path, product, multi, beta, test, version_cache, modified_files
                )

    return modified_files
