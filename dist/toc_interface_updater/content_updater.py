"""Content updating functions for TOC files."""

import re

from .constants import InterfaceDirective
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
            # Update Current Classic directive
            content = re.sub(
                InterfaceDirective.get_directive_pattern(
                    InterfaceDirective.CURRENT_CLASSIC
                ),
                f"{InterfaceDirective.CURRENT_CLASSIC} {interface}",
                content,
                flags=re.MULTILINE,
            )
            # Update Classic directive
            content = re.sub(
                InterfaceDirective.get_directive_pattern(InterfaceDirective.CLASSIC),
                f"{InterfaceDirective.CLASSIC} {interface}",
                content,
                flags=re.MULTILINE,
            )
        elif product == "wow_classic_era":
            # Update Vanilla directive
            content = re.sub(
                InterfaceDirective.get_directive_pattern(InterfaceDirective.VANILLA),
                f"{InterfaceDirective.VANILLA} {interface}",
                content,
                flags=re.MULTILINE,
            )
    else:
        # Update base interface directive
        content = re.sub(
            InterfaceDirective.get_directive_pattern(InterfaceDirective.BASE),
            f"{InterfaceDirective.BASE} {interface}",
            content,
            flags=re.MULTILINE,
        )

    return content
