"""Unit tests for file processor functions."""

import re

from toc_interface_updater.constants import TocSuffix
from toc_interface_updater.file_processor import get_product_for_file


class TestFileProcessor:
    """Test file processing functions."""

    def test_get_product_for_file_mainline(self):
        """Test product detection for Mainline files."""
        pattern = TocSuffix.get_pattern()
        product, multi = get_product_for_file("TestAddon_Mainline.toc", pattern, "wow")
        assert product == "wow"
        assert not multi

    def test_get_product_for_file_classic(self):
        """Test product detection for Classic files."""
        pattern = TocSuffix.get_pattern()
        product, multi = get_product_for_file("TestAddon_Classic.toc", pattern, "wow")
        assert product == "wow_classic"
        assert not multi

    def test_get_product_for_file_current_classic(self):
        """Test product detection for classic xpac files."""
        pattern = TocSuffix.get_pattern()
        product, multi = get_product_for_file(
            f"TestAddon_{TocSuffix.CURRENT_CLASSIC}.toc", pattern, "wow"
        )
        assert product == "wow_classic"
        assert not multi

    def test_get_product_for_file_vanilla(self):
        """Test product detection for Vanilla files."""
        pattern = TocSuffix.get_pattern()
        product, multi = get_product_for_file("TestAddon_Vanilla.toc", pattern, "wow")
        assert product == "wow_classic_era"
        assert not multi

    def test_get_product_for_file_no_match(self):
        """Test product detection for files that don't match pattern."""
        pattern = TocSuffix.get_pattern()
        product, multi = get_product_for_file("TestAddon.toc", pattern, "wow_classic")
        assert product == "wow_classic"
        assert not multi

    def test_get_product_for_file_hyphen_separator(self):
        """Test product detection with hyphen separator."""
        pattern = TocSuffix.get_pattern()
        product, multi = get_product_for_file("TestAddon-Mainline.toc", pattern, "wow")
        assert product == "wow"
        assert not multi
