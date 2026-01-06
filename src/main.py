"""Main entry point for the Pyc-Man game.

This module initializes Pygame, the game map, entities, and runs the main game loop.
"""

import sys
from typing import List

import pygame

from src.game_map import GameMap
from src.ghost import Blinky, Clyde, Ghost, GhostState, Inky, Pinky
from src.pacman import PacMan
from src.settings import (
    BLACK,
    FPS,
    GHOST_MODE_CYCLES,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TILE_SIZE,
)


def handle_ghost_release(pellets_eaten: int, timer: int, pinky, inky, clyde) -> None:
    """Handles the progressive release of ghosts based on pellets eaten and timer.

    In the original Pac-Man:
    - Blinky: starts free (already active, no release needed)
    - Pinky: exits after a short delay (60 frames / 1 second)
    - Inky: exits after 30 pellets eaten
    - Clyde: exits after 60 pellets eaten
    """
    if timer == 60:
        pinky.release_from_house()
    if pellets_eaten >= 30:
        inky.release_from_house()
    if pellets_eaten >= 60:
        clyde.release_from_house()


def get_ghost_mode(timer: int) -> str:
    """Determines the current ghost mode (SCATTER or CHASE) based on the game timer.

    Returns:
        str: "SCATTER" or "CHASE"
    """
    elapsed = timer
    for mode, duration in GHOST_MODE_CYCLES:
        if duration == -1:  # Permanent mode
            return mode
        if elapsed < duration:
            return mode
        elapsed -= duration
    return "CHASE"  # Fallback


def set_ghost_modes(ghosts: List[Ghost], mode: str, previous_mode: str) -> None:
    """Sets the mode for all ghosts and reverses their direction on mode change.

    Args:
        ghosts: List of ghost entities
        mode: New mode ("SCATTER" or "CHASE")
        previous_mode: Previous mode to detect changes
    """
    mode_changed = mode != previous_mode

    for ghost in ghosts:
        # Don't change mode if ghost is frightened or eaten
        if ghost.is_frightened or ghost.is_eaten or ghost.in_ghost_house:
            continue

        if mode == "SCATTER":
            ghost.set_state(GhostState.SCATTER, reverse_direction=mode_changed)
        elif mode == "CHASE":
            ghost.set_state(GhostState.CHASE, reverse_direction=mode_changed)


def main() -> None:  # pylint: disable=too-many-locals
    """main game loop setup"""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pyc-Man")
    clock = pygame.time.Clock()

    game_map = GameMap()

    # Pacman creation
    pacman = PacMan(
        game_map, 9 * TILE_SIZE + TILE_SIZE / 2, 16 * TILE_SIZE + TILE_SIZE / 2
    )

    # Ghost creation
    blinky = Blinky(game_map, 9.5 * TILE_SIZE, 8.5 * TILE_SIZE)
    pinky = Pinky(game_map, 8.5 * TILE_SIZE, 10.5 * TILE_SIZE)
    inky = Inky(game_map, 9.5 * TILE_SIZE, 10.5 * TILE_SIZE, blinky)
    clyde = Clyde(game_map, 10.5 * TILE_SIZE, 10.5 * TILE_SIZE)

    ghosts: List[Ghost] = [blinky, pinky, inky, clyde]

    ghost_release_timer = 0
    current_ghost_mode = "SCATTER"  # Initial mode

    # ----Main loop----------
    running = True
    while running:
        # Events handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Ghost exit timers
        ghost_release_timer += 1

        # Release ghosts from house based on pellets eaten and timer
        handle_ghost_release(
            pacman.pellets_eaten, ghost_release_timer, pinky, inky, clyde
        )

        # Update ghost modes based on timer (SCATTER/CHASE cycles)
        new_ghost_mode = get_ghost_mode(ghost_release_timer)
        if new_ghost_mode != current_ghost_mode:
            set_ghost_modes(ghosts, new_ghost_mode, current_ghost_mode)
            current_ghost_mode = new_ghost_mode

        # Pacman logic update
        pacman.handle_input()
        pacman.update(ghosts)

        # Calculate pacman directiopn for ghosts
        current_dir = pacman.direction.value if pacman.direction else (0, 0)

        for ghost in ghosts:
            ghost.update(pacman.x, pacman.y, current_dir)

        # Game Over check
        if pacman.lives <= 0:
            print("Game Over")
            running = False

        # Draw
        screen.fill(BLACK)

        game_map.draw(screen)  # map draw
        pacman.draw(screen)  # Pac-Man draw

        for ghost in ghosts:
            ghost.draw(screen)  # Ghosts draw

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
