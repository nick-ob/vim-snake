import sys

import pygame as pg

from src.game_logic import consume_food, has_failed, move_snake, random_coord
from src.rendering import draw_food, draw_grid, draw_snake


def run_game() -> None:
    pg.init()

    # window initialisation
    width = 800
    heigth = 600
    block_size = 40
    screen = pg.display.set_mode((width, heigth), pg.NOFRAME)
    pg.display.set_caption("Vim snake")

    running = True
    clock = pg.time.Clock()

    field_size: tuple[int, int] = (width // block_size, heigth // block_size)
    snake: list[tuple[int, int]] = [(7, 7), (8, 8)]
    direction: tuple[int, int] = (1, 0)
    food: tuple[int, int] = random_coord(snake, field_size)

    # game loop
    while running:
        for event in pg.event.get():
            # quitting the app
            if event.type == pg.QUIT:
                running = False

            # snake moving (vim keybinds)
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_k and direction != (0, 1):
                    direction = (0, -1)
                if event.key == pg.K_j and direction != (0, -1):
                    direction = (0, 1)
                if event.key == pg.K_h and direction != (1, 0):
                    direction = (-1, 0)
                if event.key == pg.K_l and direction != (-1, 0):
                    direction = (1, 0)

        # check game end
        if has_failed(snake, field_size):
            snake: list[tuple[int, int]] = [(7, 7), (8, 8)]
            direction: tuple[int, int] = (1, 0)
            food: tuple[int, int] = random_coord(snake, field_size)

        # check food consumption
        if snake[0] == food:
            snake = consume_food(snake)
            food = random_coord(snake, field_size)

        # rerender everything
        snake = move_snake(snake, direction)
        draw_grid(screen, width, heigth, block_size)
        draw_snake(screen, snake, block_size)
        draw_food(screen, food, block_size)

        pg.display.flip()
        clock.tick(9)

    # close the application
    pg.quit()
    sys.exit()
