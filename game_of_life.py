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
        'blinker': [(1, 0), (1, 1), (1, 2)],
        'toad': [(1, 1), (1, 2), (1, 3), (2, 0), (2, 1), (2, 2)],
        'beacon': [(0, 0), (0, 1), (1, 0), (1, 1), (2, 2), (2, 3), (3, 2), (3, 3)],
        'pulsar': [(2, 4), (2, 5), (2, 6), (2, 10), (2, 11), (2, 12),
                   (4, 2), (4, 7), (4, 9), (4, 14),
                   (5, 2), (5, 7), (5, 9), (5, 14),
                   (6, 2), (6, 7), (6, 9), (6, 14),
                   (7, 4), (7, 5), (7, 6), (7, 10), (7, 11), (7, 12),
                   (9, 4), (9, 5), (9, 6), (9, 10), (9, 11), (9, 12),
                   (10, 2), (10, 7), (10, 9), (10, 14),
                   (11, 2), (11, 7), (11, 9), (11, 14),
                   (12, 2), (12, 7), (12, 9), (12, 14),
                   (14, 4), (14, 5), (14, 6), (14, 10), (14, 11), (14, 12)]
    }
    grid = [[0 for _ in range(width)] for _ in range(height)]
    center_x = height // 2 - 3
    center_y = width // 2 - 3
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

def count_live_cells(grid):
    return sum(sum(row) for row in grid)


def run_simulation(grid, width, height, total_iterations, start_iteration=0):
    iteration = start_iteration
    stats = []
    delay = 0.5

    while iteration < total_iterations:
        clear_screen()
        live_cells = count_live_cells(grid)
        dead_cells = width * height - live_cells
        stats.append((iteration, live_cells, dead_cells))

        print(f'Iteration: {iteration + 1}/{total_iterations}')
        print(f'Live cells: {live_cells} | Dead cells: {dead_cells}')
        print_grid(grid)
        new_grid = update_grid(grid)
        iteration += 1
        grid = new_grid
        time.sleep(delay)

    clear_screen()
    live_cells = count_live_cells(grid)
    dead_cells = width * height - live_cells
    stats.append((iteration, live_cells, dead_cells))

    print(f'Final Iteration: {iteration + 1}/{total_iterations}')
    print(f'Live cells: {live_cells} | Dead cells: {dead_cells}')
    print_grid(grid)
    print("\nSimulation complete!")
    input("Press Enter to view statistics...")

    return stats, False


def display_statistics(stats):
    clear_screen()
    print("\nGame of Life - Statistics")
    print("=" * 50)
    print(f"{'Iteration':<10}{'Live Cells':<15}{'Dead Cells':<15}")
    print("-" * 50)

    for iteration, live, dead in stats:
        print(f"{iteration + 1:<10}{live:<15}{dead:<15}")


def main():
    while True:
        clear_screen()
        print('Game of Life')
        print('=' * 40)
        print('\nMain Menu:')
        print('1. Start New Game')
        print('2. Quit')

        choice = input('\nSelect option: ')

        if choice == '1':
            width = get_integer_input('\nSelect game width (at least 10): ')
            height = get_integer_input('Select game height (at least 10): ')
            iterations = get_integer_input('Enter number of iterations (at least 3): ', 3)
            while True:
                clear_screen()
                print('\nChoose starting pattern:')
                print('1. Random')
                print('2. Template: Glider')
                print('3. Template: Blinker')
                print('4. Template: Toad')
                print('5. Template: Beacon')
                print('6. Template: Pulsar')

                choice = input('Enter choice (1-7): ')
                if choice in ('1', '2', '3', '4', '5', '6', '7'):
                    break
                print('Invalid choice!')
            if choice == '1':
                grid = generate_random_grid(width, height)
            elif choice == '2':
                grid = generate_template(width, height, 'glider')
            elif choice == '3':
                grid = generate_template(width, height, 'blinker')
            elif choice == '4':
                grid = generate_template(width, height, 'toad')
            elif choice == '5':
                grid = generate_template(width, height, 'beacon')
            else:
                grid = generate_template(width, height, 'pulsar')
            stats, user_quit = run_simulation(grid, width, height, iterations)
            if not user_quit and stats:
                display_statistics(stats)
                input("\nPress Enter to return to main menu...")

        elif choice == '2':
            print("\nThanks for playing!")
            break

        else:
            print("\nInvalid choice. Press Enter to continue...")
            input()
if __name__ == '__main__':
    main()