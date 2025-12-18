"""
Test suite for GameMap class
"""

import pytest

from src.game_map import GameMap


class TestGameMap:
    """Test suite for GameMap class"""

    @pytest.fixture
    def setup_method(self):
        """Create a fresh GameMap before each test"""
        self.game_map = GameMap()

    def test_layout_is_not_empty(self):
        """Game map layout should not be empty"""
        assert len(self.game_map.layout) > 0
        assert len(self.game_map.layout[0]) > 0

    def test_initial_pellet_count(self):
        """Initial pellet count should match layout"""
        pellet_count = 0
        for row in self.game_map.layout:
            pellet_count += sum(cell in (2, 3) for cell in row)

        assert self.game_map.initial_pellets == pellet_count

    @pytest.mark.parametrize(
        "x, y, expected",
        [
            (0, 0, True),    # Wall
            (1, 1, False),   # Power pellet
            (2, 1, False),   # Pellet
            (9, 1, True),    # Wall
        ],
    )
    def test_is_wall(self, x, y, expected):
        """Test wall detection"""
        assert self.game_map.is_wall(x, y) == expected

    def test_is_wall_out_of_bounds(self):
        """Out-of-bounds positions should be walls"""
        assert self.game_map.is_wall(-1, 0)
        assert self.game_map.is_wall(0, -1)
        assert self.game_map.is_wall(999, 999)

    def test_get_cell(self):
        """Test retrieving a cell value"""
        value = self.game_map.get_cell(1, 1)
        assert value in (0, 1, 2, 3)

    def test_get_cell_out_of_bounds_returns_wall(self):
        """Out-of-bounds get_cell should return wall"""
        assert self.game_map.get_cell(-1, 0) == 1
        assert self.game_map.get_cell(0, 999) == 1

    def test_set_cell_changes_value(self):
        """Setting a cell should update the layout"""
        self.game_map.set_cell(1, 1, 0)
        assert self.game_map.get_cell(1, 1) == 0

    def test_set_cell_out_of_bounds_does_nothing(self):
        """Setting out-of-bounds should not crash"""
        self.game_map.set_cell(-1, -1, 0)
        # Test passes if no exception is raised
