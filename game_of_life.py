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
    print('⌈' + '¯' * width + '⌉')
    for row in grid:
        print('|' + ''.join('■' if cell else ' ' for cell in row) + '|')
    print('⌊' + '_' * width + '⌋')

def generate_template(width, height, template_name):
    templates = {
        'glider': [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)],
        'blinker': [(1, 0), (1, 1), (1, 2)]
    }
    grid = [[0 for _ in range(width)] for _ in range(height)]
    center_x = height // 2
    center_y = width // 2
    for cx, cy in templates[template_name]:
        x, y = center_x + cx, center_y + cy
        if 0 <= x < height and 0 <= y < width:
            grid[x][y] = 1
    return grid

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


def get_integer_input(prompt, min_value=10):
    while True:
        try:
            value = int(input(prompt))
            if value >= min_value:
                return value
            print(f'Value must be at least {min_value}!')
        except ValueError:
            print('Please use a number')


def main():
    while True:
        print('Game of Life')
        width = get_integer_input('Select games width (at least 10):')
        height = get_integer_input('Select games height (at least 10): ')
        iterations = get_integer_input('Enter a number of iterations (at least 3):', 3)

        while True:
            print('\nChoose starting pattern:')
            print('1. Random')
            print('2. Glider')
            print('3. Blinker')
            choice = input('Enter choice (1-3): ')
            if choice in ('1', '2', '3'):
                break
            print('Invalid choice!')
        if choice == '1':
            grid = generate_random_grid(width, height)
        elif choice == '2':
            grid = generate_template(width, height, 'glider')
        else:
            grid = generate_template(width, height, 'blinker')
        for iteration in range(iterations):
            clear_screen()
            print(f'Iteration: {iteration + 1}/{iterations}')
            print_grid(grid)
            grid = update_grid(grid)
            time.sleep(0.5)

        if input("\nPress Enter to restart or 'q' to quit: ").lower() == 'q':
            break
if __name__ == '__main__':
    main()