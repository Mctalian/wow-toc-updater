"""Content updating functions for TOC files."""

import re

from .types import FullProduct


def update_interface_content(
    content: str,
    product: FullProduct,
    interface: str,
    multi: bool,
    single_line_multi: bool,
) -> str:
    """Update the interface version in the content based on product and format."""
    if multi and not single_line_multi:
        if product == "wow_classic":
            content = re.sub(
                r"^(## Interface-Mists:).*$",
                f"## Interface-Mists: {interface}",
                content,
                flags=re.MULTILINE,
            )
            content = re.sub(
                r"^(## Interface-Classic:).*$",
                f"## Interface-Classic: {interface}",
                content,
                flags=re.MULTILINE,
            )
        elif product == "wow_classic_era":
            content = re.sub(
                r"^(## Interface-Vanilla:).*$",
                f"## Interface-Vanilla: {interface}",
                content,
                flags=re.MULTILINE,
            )
    else:
        content = re.sub(
            r"^(## Interface:).*$",
            f"## Interface: {interface}",
            content,
            flags=re.MULTILINE,
        )

    return content
