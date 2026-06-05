import random

def move_snake(
    snake: list[tuple[int, int]], direction: tuple[int, int]
) -> list[tuple[int, int]]:
    # move the snake into a direction
    snake_moved: list[tuple[int, int]] = []

    x_now, y_now = snake[0]
    x_mov, y_mov = direction
    snake_moved.append((x_now + x_mov, y_now + y_mov))

    for part in snake[:-1]:
        snake_moved.append(part)

    return snake_moved

def consume_food(snake: list[tuple[int, int]]) -> list[tuple[int, int]]:
    # extend the snake by food consumtion
    x_n, y_n = snake[-1]
    x_n_1, y_n_1 = snake[-2]

    direction: tuple[int, int] = (x_n - x_n_1, y_n - y_n_1)
    new: tuple[int, int] = (x_n + direction[0], y_n + direction[1])

    snake.append(new)
    return snake

def random_coord(
    snake: list[tuple[int, int]], field_size: tuple[int, int]
) -> tuple[int, int]:
    # get a random coordinate on the grid
    while True:
        x = random.randint(0, field_size[0] - 1)
        y = random.randint(0, field_size[1] - 1)
        if (x, y) not in snake:
            break

    return (x, y)

def has_failed(snake: list[tuple[int, int]], field_size: tuple[int, int]) -> bool:
    # check wether the game is over
    x, y = snake[0]
    if (x, y) in snake[1:]:
        return True

    if x < 0 or x >= field_size[0]:
        return True

    if y < 0 or y >= field_size[1]:
        return True

    return False
