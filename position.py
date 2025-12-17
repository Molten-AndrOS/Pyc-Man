from __future__ import annotations
from typing import Tuple
import math
from settings import TILE_SIZE


class Position:

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def copy(self) -> 'Position':
        return Position(self.x, self.y)

    def to_grid(self) -> Tuple[int, int]:
        """Convert pixel position to grid coordinates"""
        return int(self.x // TILE_SIZE), int(self.y // TILE_SIZE)

    def get_center(self) -> Tuple[float, float]:
        """Get center point of the tile"""
        return self.x + TILE_SIZE / 2, self.y + TILE_SIZE / 2

    def distance_to(self, other: 'Position') -> float:
        """Calculate distance to another position"""
        cx1, cy1 = self.get_center()
        cx2, cy2 = other.get_center()
        return math.sqrt((cx1 - cx2) ** 2 + (cy1 - cy2) ** 2)

