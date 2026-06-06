import pygame as pg

from src.colors import (
    BACKGROUND_DARK,
    BACKGROUND_LIGHT,
    FOOD_BORDER,
    FOOD_FILL,
    FOOD_HIGHLIGHT,
    FOOD_LEAF,
    FOOD_LEAF_BORDER,
    FOOD_STEM,
    GRID_LINE,
    SNAKE_BELLY,
    SNAKE_BORDER,
    SNAKE_EYE,
    SNAKE_FILL,
    SNAKE_HIGHLIGHT,
    SNAKE_PUPIL,
    SNAKE_TONGUE,
)


def draw_grid(screen, width: int, heigth: int, block_size: int) -> None:
    # draw an empty grid
    for x in range(0, width, block_size):
        for y in range(0, heigth, block_size):
            rect = pg.Rect(x, y, block_size, block_size)
            grid_x = x // block_size
            grid_y = y // block_size

            if (grid_x + grid_y) % 2 == 0:
                pg.draw.rect(screen, BACKGROUND_DARK, rect)
            else:
                pg.draw.rect(screen, BACKGROUND_LIGHT, rect)

            pg.draw.rect(screen, GRID_LINE, rect, 1)


def draw_snake(screen, snake: list[tuple[int, int]], block_size: int) -> None:
    # draw the snake
    if not snake:
        return

    padding = max(1, block_size // 10)
    border_width = max(1, block_size // 12)
    segment_radius = max(3, block_size // 3)
    inner_radius = max(2, segment_radius - border_width)

    def segment_rect_for(coords: tuple[int, int]) -> pg.Rect:
        x, y = coords
        rect = pg.Rect(x * block_size, y * block_size, block_size, block_size)
        return rect.inflate(-padding * 2, -padding * 2)

    def connector_rect_for(
        start: tuple[int, int],
        end: tuple[int, int],
        inset: int = 0,
    ):
        start_rect = segment_rect_for(start)
        end_rect = segment_rect_for(end)

        if start[0] == end[0]:
            top = min(start_rect.centery, end_rect.centery)
            height = abs(start_rect.centery - end_rect.centery)
            return pg.Rect(
                start_rect.left + inset,
                top,
                max(1, start_rect.width - inset * 2),
                max(1, height),
            )

        if start[1] == end[1]:
            left = min(start_rect.centerx, end_rect.centerx)
            width = abs(start_rect.centerx - end_rect.centerx)
            return pg.Rect(
                left,
                start_rect.top + inset,
                max(1, width),
                max(1, start_rect.height - inset * 2),
            )

        return None

    def draw_connectors(color: tuple[int, int, int], inset: int = 0) -> None:
        for start, end in zip(snake, snake[1:]):
            connector_rect = connector_rect_for(start, end, inset)
            if connector_rect:
                pg.draw.rect(screen, color, connector_rect)

    segment_rects = [segment_rect_for(coords) for coords in snake]

    draw_connectors(SNAKE_BORDER)
    for segment_rect in reversed(segment_rects):
        pg.draw.rect(screen, SNAKE_BORDER, segment_rect, border_radius=segment_radius)

    draw_connectors(SNAKE_FILL, border_width)
    for index, segment_rect in enumerate(segment_rects):
        fill = SNAKE_HIGHLIGHT if index == 0 else SNAKE_FILL
        inner_rect = segment_rect.inflate(-border_width * 2, -border_width * 2)
        pg.draw.rect(screen, fill, inner_rect, border_radius=inner_radius)

    belly_inset = max(block_size // 3, padding + border_width)
    for start, end in zip(snake[1:], snake[2:]):
        belly_connector = connector_rect_for(start, end, belly_inset)
        if belly_connector:
            pg.draw.rect(screen, SNAKE_BELLY, belly_connector)

    for segment_rect in segment_rects[1:]:
        belly = segment_rect.inflate(-block_size // 3, -block_size // 3)
        pg.draw.ellipse(screen, SNAKE_BELLY, belly)

    head_x, head_y = snake[0]
    head_rect = segment_rects[0]
    head_shine = pg.Rect(0, 0, max(3, block_size // 5), max(3, block_size // 5))
    head_shine.topleft = (head_rect.left + padding, head_rect.top + padding)
    pg.draw.ellipse(screen, SNAKE_HIGHLIGHT, head_shine)

    if len(snake) > 1:
        neck_x, neck_y = snake[1]
        direction_x = head_x - neck_x
        direction_y = head_y - neck_y
    else:
        direction_x = 1
        direction_y = 0

    if direction_x == 0 and direction_y == 0:
        direction_x = 1

    eye_radius = max(2, block_size // 10)
    pupil_radius = max(1, eye_radius // 2)
    eye_spacing = max(3, block_size // 5)
    eye_forward = max(3, block_size // 5)

    if direction_x != 0:
        eye_centers = [
            (
                head_rect.centerx + direction_x * eye_forward,
                head_rect.centery - eye_spacing,
            ),
            (
                head_rect.centerx + direction_x * eye_forward,
                head_rect.centery + eye_spacing,
            ),
        ]
    else:
        eye_centers = [
            (
                head_rect.centerx - eye_spacing,
                head_rect.centery + direction_y * eye_forward,
            ),
            (
                head_rect.centerx + eye_spacing,
                head_rect.centery + direction_y * eye_forward,
            ),
        ]

    for eye_center in eye_centers:
        pg.draw.circle(screen, SNAKE_EYE, eye_center, eye_radius)
        pg.draw.circle(screen, SNAKE_PUPIL, eye_center, pupil_radius)

    tongue_width = max(1, block_size // 12)
    tongue_length = max(5, block_size // 4)
    fork_length = max(3, block_size // 7)
    tongue_start = (
        head_rect.centerx + direction_x * (head_rect.width // 2 - border_width),
        head_rect.centery + direction_y * (head_rect.height // 2 - border_width),
    )
    tongue_end = (
        tongue_start[0] + direction_x * tongue_length,
        tongue_start[1] + direction_y * tongue_length,
    )
    pg.draw.line(screen, SNAKE_TONGUE, tongue_start, tongue_end, tongue_width)

    if direction_x != 0:
        fork_points = [
            (tongue_end[0] + direction_x * fork_length, tongue_end[1] - fork_length),
            (tongue_end[0] + direction_x * fork_length, tongue_end[1] + fork_length),
        ]
    else:
        fork_points = [
            (tongue_end[0] - fork_length, tongue_end[1] + direction_y * fork_length),
            (tongue_end[0] + fork_length, tongue_end[1] + direction_y * fork_length),
        ]

    for fork_point in fork_points:
        pg.draw.line(screen, SNAKE_TONGUE, tongue_end, fork_point, tongue_width)


def draw_food(screen, coords: tuple[int, int], block_size: int) -> None:
    # draw food onto the grid
    x, y = coords
    rect = pg.Rect(x * block_size, y * block_size, block_size, block_size)

    padding = max(2, block_size // 8)
    border_width = max(1, block_size // 10)
    background = BACKGROUND_DARK if (x + y) % 2 == 0 else BACKGROUND_LIGHT

    apple_rect = rect.inflate(-padding * 2, -padding * 2)
    apple_rect.top += max(1, block_size // 10)
    apple_rect.height -= max(1, block_size // 10)

    pg.draw.ellipse(screen, FOOD_FILL, apple_rect)
    pg.draw.ellipse(screen, FOOD_BORDER, apple_rect, border_width)

    notch = pg.Rect(0, 0, max(4, block_size // 4), max(3, block_size // 5))
    notch.midtop = (rect.centerx, apple_rect.top - border_width)
    pg.draw.ellipse(screen, background, notch)

    stem_width = max(2, block_size // 6)
    stem_height = max(4, block_size // 4)
    stem_top = rect.top + padding
    stem_points = [
        (rect.centerx - stem_width // 2, stem_top + stem_height),
        (rect.centerx - stem_width // 3, stem_top),
        (rect.centerx + stem_width // 2, stem_top),
        (rect.centerx + stem_width // 3, stem_top + stem_height),
    ]
    pg.draw.polygon(screen, FOOD_STEM, stem_points)

    leaf_height = max(4, block_size // 5)
    leaf_start_x = rect.centerx + stem_width // 2
    leaf_tip_x = rect.right - padding
    leaf_mid_x = (leaf_start_x + leaf_tip_x) // 2
    leaf_points = [
        (leaf_start_x, stem_top + leaf_height),
        (leaf_mid_x, stem_top),
        (leaf_tip_x, stem_top + leaf_height // 2),
        (leaf_mid_x, stem_top + leaf_height),
    ]
    pg.draw.polygon(screen, FOOD_LEAF, leaf_points)
    pg.draw.lines(screen, FOOD_LEAF_BORDER, True, leaf_points, border_width)

    highlight = pg.Rect(0, 0, max(3, block_size // 5), max(4, block_size // 3))
    highlight.center = (
        rect.left + block_size * 2 // 5,
        rect.top + block_size * 2 // 5,
    )
    pg.draw.ellipse(screen, FOOD_HIGHLIGHT, highlight)
