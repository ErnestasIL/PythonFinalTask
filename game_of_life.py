import os
import random
import time


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def generate_random_grid(width, height, probability=0.3):
    return [[1 if random.random() < probability else 0
             for _ in range(width)]
            for _ in range(height)]


def print_grid(grid):
    width = len(grid[0])
    print("⌈" + "¯" * width + "⌉")
    for row in grid:
        print("|" + "".join("■" if cell else " " for cell in row) + "|")
    print("⌊" + "_" * width + "⌋")

def count_life(grid, x, y):
    height = len(grid)
    width = len(grid[0])
    count = 0

    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            life_x, life_y = (x + i) % height, (y + j) % width
            count += grid[life_x][life_y]

    return count


def update_grid(grid):
    height = len(grid)
    width = len(grid[0])
    new_grid = [[0 for _ in range(width)] for _ in range(height)]

    for i in range(height):
        for j in range(width):
            life = count_life(grid, i, j)
            if grid[i][j] == 1:
                if life == 2 or life == 3:
                    new_grid[i][j] = 1
            else:
                if life == 3:
                    new_grid[i][j] = 1
    return new_grid


def main():
    width = 40
    height = 20
    iterations = 10
    delay = 0.5
    grid = generate_random_grid(width, height)
    for iteration in range(iterations):
        clear_screen()
        print(f"Iteration: {iteration + 1}")
        print_grid(grid)
        grid = update_grid(grid)
        if iteration < iterations - 1:
            time.sleep(delay)


if __name__ == "__main__":
    main()