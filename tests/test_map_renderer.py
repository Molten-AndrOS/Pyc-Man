"""
Basic tests for map_renderer module.
"""

import pytest

from src.map_renderer import map_renderer


class TestMapRenderer:
    """Minimal tests for map renderer."""

    def test_map_renderer_function_exists(self):
        """map_renderer function should exist."""
        assert hasattr(map_renderer, "map_renderer")

    def test_map_renderer_is_callable(self):
        """map_renderer should be callable."""
        assert callable(map_renderer.map_renderer)
