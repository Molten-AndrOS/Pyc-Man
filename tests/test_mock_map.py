"""
Shared fixtures for pytest.
"""

import pytest
from unittest.mock import MagicMock

from src.game_map import GameMap
from src.settings import TILE_SIZE


@pytest.fixture
def mock_game_map():
    """Creates a mock game map for testing."""
    m = MagicMock(spec=GameMap)
    m.width = 20
    m.height = 20
    # Default: everything is walkable
    m.is_walkable.return_value = True
    # Mock grid_to_pixel to return the exact center of the tile
    m.grid_to_pixel.side_effect = lambda gx, gy: (
        gx * TILE_SIZE + TILE_SIZE / 2,
        gy * TILE_SIZE + TILE_SIZE / 2,
    )
    # Default: empty cell
    m.get_cell.return_value = 0
    return m
