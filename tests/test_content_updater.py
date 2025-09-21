"""Unit tests for content updater functions."""

from toc_interface_updater.content_updater import update_interface_content


class TestContentUpdater:
    """Test content updating functions."""

    def test_update_interface_content_single_line(self):
        """Test updating single line interface."""
        content = "## Interface: 100000\n## Title: Test Addon"
        result = update_interface_content(content, "wow", "110000", False, False)
        expected = "## Interface: 110000\n## Title: Test Addon"
        assert result == expected

    def test_update_interface_content_wow_classic_multi(self):
        """Test updating WoW Classic multi-line interfaces."""
        content = """## Interface-Mists: 40400
## Interface-Classic: 11503
## Title: Test Addon"""
        result = update_interface_content(
            content, "wow_classic", "40401, 11504", True, False
        )
        expected = """## Interface-Mists: 40401, 11504
## Interface-Classic: 40401, 11504
## Title: Test Addon"""
        assert result == expected

    def test_update_interface_content_wow_classic_era_multi(self):
        """Test updating WoW Classic Era multi-line interface."""
        content = "## Interface-Vanilla: 11503\n## Title: Test Addon"
        result = update_interface_content(
            content, "wow_classic_era", "11504", True, False
        )
        expected = "## Interface-Vanilla: 11504\n## Title: Test Addon"
        assert result == expected

    def test_update_interface_content_single_line_multi_mode(self):
        """Test updating when in single line multi mode."""
        content = "## Interface: 110000, 110001\n## Title: Test Addon"
        result = update_interface_content(content, "wow", "110002, 110003", False, True)
        expected = "## Interface: 110002, 110003\n## Title: Test Addon"
        assert result == expected

    def test_update_interface_content_no_change_needed(self):
        """Test when no interface line exists."""
        content = "## Title: Test Addon\n## Author: Test"
        result = update_interface_content(content, "wow", "110000", False, False)
        # Should return same content since no interface line to update
        assert result == content
