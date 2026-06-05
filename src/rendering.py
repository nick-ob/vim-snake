import pygame as pg

from src.colors import (
    BACKGROUND_DARK,
    BACKGROUND_LIGHT,
    FOOD_BORDER,
    FOOD_FILL,
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
    pg.draw.rect(screen, FOOD_FILL, rect)
    pg.draw.rect(screen, FOOD_BORDER, rect, 2)
