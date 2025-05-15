import pygame
import sys
import random
import config

UP = 'up'
DOWN = 'down'
RIGHT = 'right'
LEFT = 'left'
direction = 'right'

def close_game():
    pygame.quit()
    exit()

def lose_game(score):
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
                close_game()
        font_for_game_over = pygame.font.Font('simkai.ttf', 52)
        last_info_label = font_for_game_over.render(f'GAME OVER. Score: {score}', True, (255, 255, 255))
        rect = last_info_label.get_rect()
        rect.center = (config.SCREENWIDTH // 2, config.SCREENHEIGHT // 2)
        screen.blit(last_info_label, rect)
        pygame.display.update()

def draw_grid():
    for x in range(0, config.SCREENWIDTH, config.CELLSIZE):
        pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, config.SCREENHEIGHT))
    for y in range(0, config.SCREENHEIGHT, config.CELLSIZE):
        pygame.draw.line(screen, (40, 40, 40), (0, y), (config.SCREENWIDTH, y))

def show_snake(snake_coords):
    x = snake_coords[0]['x'] * config.CELLSIZE
    y = snake_coords[0]['y'] * config.CELLSIZE
    head_rect = pygame.Rect(x, y, config.CELLSIZE, config.CELLSIZE)
    pygame.draw.rect(screen, (0, 80, 255), head_rect)
    head_inner_rect = pygame.Rect(x + 4, y + 4, config.CELLSIZE - 8, config.CELLSIZE - 8)
    pygame.draw.rect(screen, (0, 80, 255), head_inner_rect)
    for snake_coord in snake_coords[1:]:
        x = snake_coord['x'] * config.CELLSIZE
        y = snake_coord['y'] * config.CELLSIZE
        rect = pygame.Rect(x, y, config.CELLSIZE, config.CELLSIZE)
        pygame.draw.rect(screen, (0, 155, 0), rect)
        inner_rect = pygame.Rect(x + 4, y + 4, config.CELLSIZE - 8, config.CELLSIZE - 8)
        pygame.draw.rect(screen, (0, 255, 0), inner_rect)

def get_apple_location(snake_coords):
    flag = True
    while flag:
        apple_location = {
            'x': random.randint(0, config.MATRIX_W - 1),
            'y': random.randint(0, config.MATRIX_H - 1)
        }
        if apple_location not in snake_coords:
            flag = False
    return apple_location

def show_apple(apple_location):
    x = apple_location['x'] * config.CELLSIZE
    y = apple_location['y'] * config.CELLSIZE
    rect = pygame.Rect(x, y, config.CELLSIZE, config.CELLSIZE)
    pygame.draw.rect(screen, (255, 0, 0), rect)

def show_score(score, temp_FPS):
    score_render = default_font.render(f'Score: {score}, FPS: {temp_FPS}', True, (255, 255, 255))
    rect = score_render.get_rect()
    rect.topleft = (config.SCREENWIDTH - 220, 10)
    screen.blit(score_render, rect)


def is_cell_free(idx, snake_coords):
    location_x = idx % config.MATRIX_W
    location_y = idx // config.MATRIX_W
    idx = {'x': location_x, 'y': location_y}
    return {idx not in snake_coords}

def reset_board(snake_coords, apple_location, board):
    temp_board = board[:]
    apple_idx = apple_location['x'] + apple_location['y'] * config.MATRIX_W
    for i in range(config.MATRIX):
        if i == apple_idx:
            temp_board[i] = config.FOODNUM
        elif is_cell_free(i, snake_coords):
            temp_board[i] = config.SPACE_NUM
        else:
            temp_board[i] = config.SNAKE_NUM
    return temp_board

def update_shake_head(snake_coords):
    if direction == UP:
        new_head = {
            'x': snake_coords[0]['x'],
            'y': snake_coords[0]['y'] - 1
        }
    elif direction == DOWN:
        new_head = {
            'x': snake_coords[0]['x'],
            'y': snake_coords[0]['y'] + 1
        }
    elif direction == RIGHT:
        new_head = {
            'x': snake_coords[0]['x'] + 1,
            'y': snake_coords[0]['y']
        }
    else:
        new_head = {
            'x': snake_coords[0]['x'] - 1,
            'y': snake_coords[0]['y']
        }
    return new_head

def check_collapse(snake_coords):
    if (snake_coords[0]['x'] < 0 or snake_coords[0]['x'] >= config.MATRIX_W
            or snake_coords[0]['y'] < 0 or snake_coords[0]['y'] >= config.MATRIX_H
            or snake_coords[0] in snake_coords[1:]):
        close_game()
def run_game():
    global direction
    temp_FPS = config.FPS
    board = [0] * config.MATRIX
    start_x = random.randint(5, config.MATRIX_W)
    start_y = random.randint(5, config.MATRIX_H)
    snake_coords = [{'x': start_x, 'y': start_y},
                    {'x': start_x-1, 'y': start_y},
                    {'x': start_x-2, 'y': start_y}]
    apple_location = get_apple_location(snake_coords)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    close_game()
                elif event.key == pygame.K_UP and direction != DOWN:
                    direction = UP
                elif event.key == pygame.K_DOWN and direction != UP:
                    direction = DOWN
                elif event.key == pygame.K_LEFT and direction != RIGHT:
                    direction = LEFT
                elif event.key == pygame.K_RIGHT and direction != LEFT:
                    direction = RIGHT
        if direction == UP:
            new_head = {'x': snake_coords[0]['x'], 'y': snake_coords[0]['y'] - 1}
        elif direction == DOWN:
            new_head = {'x': snake_coords[0]['x'], 'y': snake_coords[0]['y'] + 1}
        elif direction == LEFT:
            new_head = {'x': snake_coords[0]['x'] - 1, 'y': snake_coords[0]['y']}
        elif direction == RIGHT:
            new_head = {'x': snake_coords[0]['x'] + 1, 'y': snake_coords[0]['y']}

        if (new_head['x'] < 0):
            new_head['x'] = config.MATRIX_W
        elif new_head['x'] >= config.MATRIX_W:
            new_head['x'] = 0
        elif new_head['y'] < 0:
            new_head['y'] = config.MATRIX_H
        elif new_head['y'] >= config.MATRIX_H:
            new_head['y'] = 0

        if new_head in snake_coords[1:]:
            lose_game(len(snake_coords) - 3)

        snake_coords.insert(0, new_head)
        if snake_coords[0] == apple_location:
            apple_location = get_apple_location(snake_coords)
            if (len(snake_coords) - 3) % 9 == 0:
                temp_FPS += 1
        else:
            snake_coords.pop()
        screen.fill(config.BG_COLOR)
        draw_grid()
        show_snake(snake_coords)
        show_apple(apple_location)
        show_score(len(snake_coords) - 3, temp_FPS)
        pygame.display.update()
        clock.tick(temp_FPS)


def show_end_interface():
    pass

def main():
    global screen, default_font, clock
    pygame.init()
    screen = pygame.display.set_mode((config.SCREENWIDTH, config.SCREENHEIGHT))
    pygame.display.set_caption('Snake')
    default_font = pygame.font.Font('simkai.ttf', 18)
    clock = pygame.time.Clock()
    while True:
        run_game()
        show_end_interface()

if __name__ == '__main__':
    main()