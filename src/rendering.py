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
    SNAKE_BORDER,
    SNAKE_FILL,
)


def draw_grid(screen, width: int, heigth: int, block_size: int) -> None:
    # draw an empty grid
    for x in range(0, width, block_size):
        for y in range(0, heigth, block_size):
            rect = pg.Rect(x, y, block_size, block_size)
            if (x // block_size + y // block_size) % 2 == 0:
                pg.draw.rect(screen, BACKGROUND_DARK, rect)
            else:
                pg.draw.rect(screen, BACKGROUND_LIGHT, rect)
            pg.draw.rect(screen, GRID_LINE, rect, 1)


def draw_snake(screen, snake: list[tuple[int, int]], block_size: int) -> None:
    # draw the snake
    for x, y in snake:
        rect = pg.Rect(x * block_size, y * block_size, block_size, block_size)
        pg.draw.rect(screen, SNAKE_FILL, rect)
        pg.draw.rect(screen, SNAKE_BORDER, rect, 1)


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
