"""Unit tests for version resolver functions."""

from toc_interface_updater.version_resolver import (
    detect_existing_versions,
    get_beta_products,
    get_test_products,
)


class TestProductMapping:
    """Test product mapping functions."""

    def test_get_beta_products_wow(self):
        """Test beta products for wow."""
        result = get_beta_products("wow")
        assert result == ["wow_beta"]

    def test_get_beta_products_wow_classic(self):
        """Test beta products for wow_classic."""
        result = get_beta_products("wow_classic")
        assert result == ["wow_classic_beta"]

    def test_get_beta_products_wow_classic_era(self):
        """Test beta products for wow_classic_era."""
        result = get_beta_products("wow_classic_era")
        assert result == []

    def test_get_test_products_wow(self):
        """Test test products for wow."""
        result = get_test_products("wow")
        assert result == ["wowt", "wowxptr"]

    def test_get_test_products_wow_classic(self):
        """Test test products for wow_classic."""
        result = get_test_products("wow_classic")
        assert result == ["wow_classic_ptr"]

    def test_get_test_products_wow_classic_era(self):
        """Test test products for wow_classic_era."""
        result = get_test_products("wow_classic_era")
        assert result == ["wow_classic_era_ptr"]


class TestVersionDetection:
    """Test version detection functions."""

    def test_detect_existing_versions_single_line_multi(self):
        """Test detection of single line multi-version interface."""
        content = "## Interface: 110000, 110001\n## Title: Test Addon"
        versions, is_single_multi = detect_existing_versions(content, "wow", False)
        assert versions == {"110000", "110001"}
        assert is_single_multi

    def test_detect_existing_versions_single_line_not_multi(self):
        """Test detection of single line interface when multi is requested."""
        content = "## Interface: 110000, 110001\n## Title: Test Addon"
        versions, is_single_multi = detect_existing_versions(content, "wow", True)
        # When multi=True is requested but we have single line multi,
        # the function returns empty set because it expects multi-line format
        assert versions == set()
        assert not is_single_multi

    def test_detect_existing_versions_wow_classic_mists(self):
        """Test detection of WoW Classic Mists interface."""
        content = "## Interface-Mists: 40400\n## Title: Test Addon"
        versions, is_single_multi = detect_existing_versions(
            content, "wow_classic", True
        )
        assert versions == {"40400"}
        assert not is_single_multi

    def test_detect_existing_versions_wow_classic_both(self):
        """Test detection of both Mists and Classic interfaces."""
        content = """## Interface-Mists: 40400
## Interface-Classic: 11503
## Title: Test Addon"""
        versions, is_single_multi = detect_existing_versions(
            content, "wow_classic", True
        )
        assert versions == {"40400", "11503"}
        assert not is_single_multi

    def test_detect_existing_versions_vanilla(self):
        """Test detection of Vanilla interface."""
        content = "## Interface-Vanilla: 11503\n## Title: Test Addon"
        versions, is_single_multi = detect_existing_versions(
            content, "wow_classic_era", True
        )
        assert versions == {"11503"}
        assert not is_single_multi

    def test_detect_existing_versions_no_versions(self):
        """Test when no versions are detected."""
        content = "## Title: Test Addon\n## Author: Test"
        versions, is_single_multi = detect_existing_versions(content, "wow", False)
        assert versions == set()
        assert not is_single_multi
