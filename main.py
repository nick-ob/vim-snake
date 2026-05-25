import pygame as pg
import sys
import random

def draw_grid(screen, width: int, heigth: int, block_size: int) -> None:
    screen.fill((50, 50, 50))
    for x in range(0, width, block_size):
        for y in range(0, heigth, block_size):
            rect = pg.Rect(x, y, block_size, block_size)
            pg.draw.rect(screen, (255, 255, 255), rect, 1)

def draw_snake(snake: list[tuple[int, int]], block_size) -> None:
    for x, y in snake:
        rect = pg.Rect(x * block_size, y * block_size, block_size, block_size)
        pg.draw.rect(screen, (50, 200, 50), rect)

def move_snake(snake: list[tuple[int, int]], direction: tuple[int, int]) -> list[tuple[int, int]]:
    snake_moved: list[tuple[int, int]] = []

    x_now, y_now = snake[0]
    x_mov, y_mov = direction
    snake_moved.append((x_now + x_mov, y_now + y_mov))

    for part in snake[:-1]:
        snake_moved.append(part)

    return snake_moved

def draw_food(screen, coords: tuple[int, int], block_size: int) -> None:
    x, y = coords
    rect = pg.Rect(x * block_size, y * block_size, block_size, block_size)
    pg.draw.rect(screen, (200, 50, 50), rect)

def random_coord(field_size: tuple[int, int]) -> tuple[int, int]:
    x = random.randint(0, field_size[0] - 1)
    y = random.randint(0, field_size[1] - 1)

    return (x, y)

pg.init()

width = 800
heigth = 600
block_size = 40
screen = pg.display.set_mode((width, heigth))
pg.display.set_caption("Vim snake")

running = True
clock = pg.time.Clock()

field_size: tuple[int, int] = (width // block_size, heigth // block_size)
snake: list[tuple[int, int]] = [(int((width / block_size) / 2), int((heigth / block_size) / 2))]
direction: tuple[int, int] = (1, 0)
food: tuple[int, int] = random_coord(field_size)

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_k and direction != (0, 1):
                direction = (0, -1)
            if event.key == pg.K_j and direction != (0, -1):
                direction = (0, 1)
            if event.key == pg.K_h and direction != (1, 0):
                direction = (-1, 0)
            if event.key == pg.K_l and direction != (-1, 0):
                direction = (1, 0)

    if snake[0] == food:
        food = random_coord(field_size)
        print(food)

    snake = move_snake(snake, direction)
    draw_grid(screen, width, heigth, block_size)
    draw_snake(snake, block_size)
    draw_food(screen, food, block_size)

    pg.display.flip()
    clock.tick(10)

pg.quit()
sys.exit()
