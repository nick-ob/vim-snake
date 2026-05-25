import pygame as pg
import sys

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

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    draw_grid(screen, width, heigth, block_size)
    draw_snake(snake, block_size)

    pg.display.flip()
    clock.tick()

pg.quit()
sys.exit()
