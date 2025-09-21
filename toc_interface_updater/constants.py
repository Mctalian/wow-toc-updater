"""Constants and string definitions for the TOC interface updater."""

import re
from typing import Dict


class InterfaceDirective:
    """Interface directive definitions for TOC files."""

    # Base interface directive (used for retail/mainline)
    BASE = "## Interface:"

    # Specific flavor directives
    MAINLINE = "## Interface-Mainline:"
    MISTS = "## Interface-Mists:"
    CATA = "## Interface-Cata:"
    WRATH = "## Interface-Wrath:"
    WOTLK = "## Interface-WOTLK:"  # Legacy name for Wrath
    TBC = "## Interface-TBC:"
    BCC = "## Interface-BCC:"  # Legacy name for TBC
    VANILLA = "## Interface-Vanilla:"
    CLASSIC = "## Interface-Classic:"
    CURRENT_CLASSIC = MISTS

    # All currently used/supported directives as a list for iteration
    ALL_DIRECTIVES = [BASE, MAINLINE, VANILLA, CLASSIC, CURRENT_CLASSIC]

    @classmethod
    def get_directive_pattern(cls, directive: str) -> str:
        """Get regex pattern for a specific directive."""
        # Escape the directive for use in regex and make it match the full line
        escaped = re.escape(directive)
        return f"^({escaped}).*$"

    @classmethod
    def get_all_patterns(cls) -> Dict[str, str]:
        """Get regex patterns for all directives."""
        return {
            directive: cls.get_directive_pattern(directive)
            for directive in cls.ALL_DIRECTIVES
        }


class TocSuffix:
    """TOC file suffix definitions for different WoW flavors."""

    # TOC file suffixes used in filename patterns
    MAINLINE = "Mainline"  # Retail including Plunderstorm
    STANDARD = "Standard"  # Retail minus Plunderstorm
    WOWLABS = "WoWLabs"  # just Plunderstorm
    MISTS = "Mists"
    CATA = "Cata"
    WRATH = "Wrath"
    WOTLK = "WOTLK"  # Legacy name for Wrath
    TBC = "TBC"
    BCC = "BCC"  # Legacy name for TBC
    VANILLA = "Vanilla"
    CLASSIC = "Classic"
    CURRENT_CLASSIC = MISTS

    # All currently used/supported suffixes as a list for iteration
    ALL_SUFFIXES = [MAINLINE, CLASSIC, CURRENT_CLASSIC, VANILLA]

    # Mapping of suffixes to their corresponding products
    SUFFIX_TO_PRODUCT = {
        MAINLINE: "wow",
        CLASSIC: "wow_classic",
        MISTS: "wow_classic",
        VANILLA: "wow_classic_era",
    }

    @classmethod
    def get_pattern(cls) -> re.Pattern:
        """Get compiled regex pattern for matching TOC suffixes."""
        suffix_pattern = "|".join(cls.ALL_SUFFIXES)
        return re.compile(f"[-_]({suffix_pattern})\\.toc$")

    @classmethod
    def get_product_for_suffix(cls, suffix: str) -> str:
        """Get the product type for a given suffix."""
        return cls.SUFFIX_TO_PRODUCT.get(suffix, "wow")
