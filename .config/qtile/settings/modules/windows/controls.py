from libqtile.lazy import lazy
def _check_window_move(qtile, change_x: int, change_y: int) -> tuple[int, int]:

    window = qtile.current_window
    if not window or not window.floating:
        return change_x, change_y

    # Get window's current position and dimensions
    win_x, win_y = window.x, window.y
    win_width, win_height = window.width, window.height

    # Find the screen where the window is currently located
    current_window_screen = qtile.current_screen

    screen_x, screen_y = current_window_screen.x, current_window_screen.y
    screen_width, screen_height = current_window_screen.width, current_window_screen.height

    # Calculate the new intended position of the window
    new_x = win_x + change_x
    new_y = win_y + change_y

    # Check for adjacent screens
    has_left = any(screen.x + screen.width == screen_x for screen in qtile.screens if screen != current_window_screen)
    has_right = any(screen.x == screen_x + screen_width for screen in qtile.screens if screen != current_window_screen)
    has_top = any(screen.y + screen.height == screen_y for screen in qtile.screens if screen != current_window_screen)
    has_bottom = any(screen.y == screen_y + screen_height for screen in qtile.screens if screen != current_window_screen)

    # Check horizontal boundaries
    if new_x < screen_x and not has_left:
        # Restrict to left edge
        change_x = screen_x - win_x
    elif new_x + win_width > screen_x + screen_width and not has_right:
        # Restrict to right edge
        change_x = (screen_x + screen_width) - (win_x + win_width) - 7

    # Check vertical boundaries
    if new_y < screen_y and not has_top:
        # Restrict to top edge
        change_y = screen_y - win_y
    elif new_y + win_height > screen_y + screen_height and not has_bottom:
        # Restrict to botton edge
        change_y = (screen_y + screen_height) - (win_y + win_height) - 7

    return change_x, change_y


@lazy.function
def move_window(qtile, direction: str) -> None:
    x = 0
    y = 0
    window = qtile.current_window
    layout = qtile.current_layout

    if window.floating:
        match direction:
            case "left":
                x = -1000
            case "right":
                x = 1000
            case "up":
                y = -1000
            case "down":
                y = 1000

        x, y = _check_window_move(qtile, x, y)

        window.move_floating(x, y)
    elif direction in ["left", "right", "up", "down"]:
        match direction:
            case "left":
                layout.shuffle_left()
            case "right":
                layout.shuffle_right()
            case "up":
                layout.shuffle_up()
            case "down":
                layout.shuffle_down()

@lazy.function
def resize_window(qtile, direction: str, amount: int) -> None:
    x = 0
    y = 0
    window = qtile.current_window
    layout = qtile.current_layout

    if window.floating:
        match direction:
            case "left":
                x = -100
            case "right":
                x = 100
            case "up":
                y = -100
            case "down":
                y = 100
            case _:
                x = 0
                y = 0
        window.resize_floating(x, y)
    elif direction in ["left", "right", "up", "down"]:
        match direction:
            case "left":
                layout.grow_left()
            case "right":
                layout.grow_right()
            case "up":
                layout.grow_up()
            case "down":
                layout.grow_down()
