"""Unit tests for content updater functions."""

from toc_interface_updater.constants import InterfaceDirective
from toc_interface_updater.content_updater import update_interface_content


class TestContentUpdater:
    """Test content updating functions."""

    def test_update_interface_content_single_line(self):
        """Test updating single line interface."""
        content = f"{InterfaceDirective.BASE} 100000\n## Title: Test Addon"
        result = update_interface_content(content, "wow", "110000", False, False)
        expected = f"{InterfaceDirective.BASE} 110000\n## Title: Test Addon"
        assert result == expected

    def test_update_interface_content_wow_classic_multi(self):
        """Test updating WoW Classic multi-line interfaces."""
        content = f"""{InterfaceDirective.CURRENT_CLASSIC} 40400
{InterfaceDirective.CLASSIC} 11503
## Title: Test Addon"""
        result = update_interface_content(
            content, "wow_classic", "40401, 11504", True, False
        )
        expected = f"""{InterfaceDirective.CURRENT_CLASSIC} 40401, 11504
{InterfaceDirective.CLASSIC} 40401, 11504
## Title: Test Addon"""
        assert result == expected

    def test_update_interface_content_wow_classic_era_multi(self):
        """Test updating WoW Classic Era multi-line interface."""
        content = f"{InterfaceDirective.VANILLA} 11503\n## Title: Test Addon"
        result = update_interface_content(
            content, "wow_classic_era", "11504", True, False
        )
        expected = f"{InterfaceDirective.VANILLA} 11504\n## Title: Test Addon"
        assert result == expected

    def test_update_interface_content_single_line_multi_mode(self):
        """Test updating when in single line multi mode."""
        content = f"{InterfaceDirective.BASE} 110000, 110001\n## Title: Test Addon"
        result = update_interface_content(content, "wow", "110002, 110003", False, True)
        expected = f"{InterfaceDirective.BASE} 110002, 110003\n## Title: Test Addon"
        assert result == expected

    def test_update_interface_content_no_change_needed(self):
        """Test when no interface line exists."""
        content = "## Title: Test Addon\n## Author: Test"
        result = update_interface_content(content, "wow", "110000", False, False)
        # Should return same content since no interface line to update
        assert result == content
