from typing import List

from .cli import main
from .content_updater import update_interface_content
from .file_processor import write_file_if_changed
from .types import (
    FullProduct,
    VersionCache,
)
from .version_resolver import (
    collect_all_versions,
    detect_existing_versions,
    get_versions_from_detected,
)

# ANSI escape sequences for colors and formatting
RESET = "\033[0m"
BOLD = "\033[1m"
LIGHT_BLUE = "\033[94m"
GREEN = "\033[32m"
YELLOW = "\033[33m"


def update_versions(
    file: str,
    product: FullProduct,
    multi: bool,
    beta: bool,
    test: bool,
    version_cache: VersionCache,
    modified_files: List[str],
):
    print(
        f"{LIGHT_BLUE}Checking {RESET}{BOLD}{file}{RESET}{LIGHT_BLUE} ({product})...{RESET} ",
        end="",
    )

    # Read and normalize file content
    with open(file, "r") as f:
        original_content = f.read()
    original_content_normalized = original_content.replace("\r\n", "\n").replace(
        "\r", "\n"
    )

    # Get all versions for this product
    versions = collect_all_versions(product, beta, test, version_cache)
    interface = ", ".join(sorted(versions, key=lambda x: int(x)))
    print(f"Determined interface versions: {interface}")

    # Detect existing versions and determine format
    detected_versions, single_line_multi = detect_existing_versions(
        original_content_normalized, product, multi
    )

    if detected_versions:
        versions = get_versions_from_detected(
            detected_versions, beta, test, version_cache
        )
        interface = ", ".join(sorted(versions, key=lambda x: int(x)))

    # Update the content with new interface versions
    updated_content = update_interface_content(
        original_content_normalized, product, interface, multi, single_line_multi
    )

    # Write file if changed
    write_file_if_changed(
        file, original_content_normalized, updated_content, modified_files
    )


if __name__ == "__main__":
    main()
