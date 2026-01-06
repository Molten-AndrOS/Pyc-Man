"""
Basic tests for main module
"""

from pytest_mock import MockerFixture

from src.main import handle_ghost_release, main


def test_ghost_release_logic(mocker: MockerFixture):
    """Tests that ghosts are released at the correct time using pytest-mock.

    New behavior:
    - Blinky: starts free (not in this function anymore)
    - Pinky: exits after 60 frames (1 second)
    - Inky: exits after 30 pellets eaten
    - Clyde: exits after 60 pellets eaten
    """
    # Create Mocks for ghosts (no blinky anymore)
    pinky = mocker.Mock()
    inky = mocker.Mock()
    clyde = mocker.Mock()

    # Test Frame 59, 0 pellets (No exits yet)
    handle_ghost_release(0, 59, pinky, inky, clyde)
    pinky.release_from_house.assert_not_called()

    # Test Frame 60, 0 pellets (Pinky exits)
    handle_ghost_release(0, 60, pinky, inky, clyde)
    pinky.release_from_house.assert_called_once()

    # Test Frame 100, 29 pellets (No Inky yet)
    handle_ghost_release(29, 100, pinky, inky, clyde)
    inky.release_from_house.assert_not_called()

    # Test Frame 100, 30 pellets (Inky exits)
    handle_ghost_release(30, 100, pinky, inky, clyde)
    inky.release_from_house.assert_called_once()

    # Test Frame 100, 59 pellets (No Clyde yet)
    handle_ghost_release(59, 100, pinky, inky, clyde)
    clyde.release_from_house.assert_not_called()

    # Test Frame 100, 60 pellets (Clyde exits)
    handle_ghost_release(60, 100, pinky, inky, clyde)
    clyde.release_from_house.assert_called_once()


class TestMain:
    """Minimal tests for main function"""

    def test_main_function_exists(self):
        """main function should exist"""
        assert main is not None

    def test_main_is_callable(self):
        """main should be callable"""
        assert callable(main)
