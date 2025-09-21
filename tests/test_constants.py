"""Unit tests for constants and TOC suffix functionality."""

import re

from toc_interface_updater.constants import InterfaceDirective, TocSuffix


class TestInterfaceDirective:
    """Test interface directive constants and utilities."""

    def test_all_directives_defined(self):
        """Test that all expected directives are defined."""
        expected_directives = [
            "## Interface:",
            f"## Interface-{TocSuffix.MAINLINE}:",
            f"## Interface-{TocSuffix.VANILLA}:",
            f"## Interface-{TocSuffix.CLASSIC}:",
            f"## Interface-{TocSuffix.CURRENT_CLASSIC}:",
        ]
        assert InterfaceDirective.ALL_DIRECTIVES == expected_directives

    def test_directive_pattern_generation(self):
        """Test that directive patterns are generated correctly."""
        pattern = InterfaceDirective.get_directive_pattern(InterfaceDirective.BASE)
        # Pattern should be escaped for regex safety
        assert pattern == "^(\\#\\#\\ Interface:).*$"

        # Test that it matches valid content
        regex = re.compile(pattern, re.MULTILINE)
        assert regex.search("## Interface: 110000")
        assert not regex.search("## Title: My Addon")


class TestTocSuffix:
    """Test TOC suffix constants and utilities."""

    def test_all_suffixes_defined(self):
        """Test that all expected suffixes are defined."""
        expected_suffixes = ["Mainline", "Classic", "Mists", "Vanilla"]
        assert TocSuffix.ALL_SUFFIXES == expected_suffixes

    def test_suffix_to_product_mapping(self):
        """Test suffix to product mapping."""
        assert TocSuffix.get_product_for_suffix(TocSuffix.MAINLINE) == "wow"
        assert TocSuffix.get_product_for_suffix(TocSuffix.CLASSIC) == "wow_classic"
        assert (
            TocSuffix.get_product_for_suffix(TocSuffix.CURRENT_CLASSIC) == "wow_classic"
        )
        assert TocSuffix.get_product_for_suffix(TocSuffix.VANILLA) == "wow_classic_era"
        assert TocSuffix.get_product_for_suffix("Unknown") == "wow"  # Default

    def test_toc_pattern_matching(self):
        """Test that TOC pattern matches expected file names."""
        pattern = TocSuffix.get_pattern()

        # Should match
        assert pattern.search(f"MyAddon-{TocSuffix.CLASSIC}.toc")
        assert pattern.search(f"MyAddon_{TocSuffix.VANILLA}.toc")
        assert pattern.search(f"MyAddon-{TocSuffix.MAINLINE}.toc")
        assert pattern.search(f"MyAddon_{TocSuffix.CURRENT_CLASSIC}.toc")

        # Should not match
        assert not pattern.search("MyAddon.toc")
        assert not pattern.search("MyAddon-Unknown.toc")
        assert not pattern.search("MyAddon-Classic.lua")

    def test_suffix_extraction(self):
        """Test extracting suffix from file names."""
        pattern = TocSuffix.get_pattern()

        match = pattern.search(f"MyAddon-{TocSuffix.CLASSIC}.toc")
        assert match.group(1) == "Classic"

        match = pattern.search(f"MyAddon_{TocSuffix.VANILLA}.toc")
        assert match.group(1) == "Vanilla"
