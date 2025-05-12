import sys
import random
import pygame


ERR = -404
SCREENWIDTH = 300
SCREENHEIGHT = 260
FPS = 100
CELLSIZE = 20
SCREENWIDTH % CELLSIZE == 0
assert SCREENHEIGHT % CELLSIZE == 0
MATRIX_W = int(SCREENWIDTH/CELLSIZE)
MATRIX_H = int(SCREENHEIGHT/CELLSIZE)
MATRIX_SIZE = MATRIX_W * MATRIX_H
BGCOLOR = (0, 0, 0)
HEADINDEX = 0
BESTMOVE = ERR
FOODNUM = 0
SPACENUM = (MATRIX_W + 1) * (MATRIX_H + 1)
SNAKENUM = 2 * SPACENUM
MOVEDIRECTIONS = {
					'left': -1,
					'right': 1,
					'up': -MATRIX_W,
					'down': MATRIX_W
					}


def CloseGame():
	pygame.quit()
	sys.exit()


def ShowScore(score):
	score_render = default_font.render('score: %s' % (score), True, (255, 255, 255))
	rect = score_render.get_rect()
	rect.topleft = (SCREENWIDTH-120, 10)
	screen.blit(score_render, rect)

def GetAppleLocation(snake_coords):
	flag = True
	while flag:
		apple_location = {'x': random.randint(0, MATRIX_W-1), 'y': random.randint(0, MATRIX_H-1)}
		if apple_location not in snake_coords:
			flag = False
	return apple_location

def ShowApple(coord):
	x = coord['x'] * CELLSIZE
	y = coord['y'] * CELLSIZE
	rect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
	pygame.draw.rect(screen, (255, 0, 0), rect)

def ShowSnake(coords):
	x = coords[0]['x'] * CELLSIZE
	y = coords[0]['y'] * CELLSIZE
	head_rect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
	pygame.draw.rect(screen, (0, 80, 255), head_rect)
	head_inner_rect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
	pygame.draw.rect(screen, (0, 80, 255), head_inner_rect)
	for coord in coords[1:]:
		x = coord['x'] * CELLSIZE
		y = coord['y'] * CELLSIZE
		rect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
		pygame.draw.rect(screen, (0, 155, 0), rect)
		inner_rect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
		pygame.draw.rect(screen, (0, 255, 0), inner_rect)

def drawGrid():
	for x in range(0, SCREENWIDTH, CELLSIZE):
		pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, SCREENHEIGHT))
	for y in range(0, SCREENHEIGHT, CELLSIZE):
		pygame.draw.line(screen, (40, 40, 40), (0, y), (SCREENWIDTH, y))

def ShowEndInterface():
	title_font = pygame.font.Font('simkai.ttf', 100)
	title_game = title_font.render('Game', True, (233, 150, 122))
	title_over = title_font.render('Over', True, (233, 150, 122))
	game_rect = title_game.get_rect()
	over_rect = title_over.get_rect()
	game_rect.midtop = (SCREENWIDTH/2, 70)
	over_rect.midtop = (SCREENWIDTH/2, game_rect.height+70+25)
	screen.blit(title_game, game_rect)
	screen.blit(title_over, over_rect)
	pygame.display.update()
	pygame.time.wait(500)
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
				CloseGame()

def IsCellFree(idx, psnake):
	location_x = idx % MATRIX_W
	location_y = idx // MATRIX_W
	idx = {'x': location_x, 'y': location_y}
	return (idx not in psnake)

def ResetBoard(psnake, pboard, pfood):
	temp_board = pboard[:]
	pfood_idx = pfood['x'] + pfood['y'] * MATRIX_W
	for i in range(MATRIX_SIZE):
		if i == pfood_idx:
			temp_board[i] = FOODNUM
		elif IsCellFree(i, psnake):
			temp_board[i] = SPACENUM
		else:
			temp_board[i] = SNAKENUM
	return temp_board

def isMovePossible(idx, move_direction):
	flag = False
	if move_direction == 'left':
		if idx % MATRIX_W > 0: flag = True
		else: flag = False
	elif move_direction == 'right':
		if idx % MATRIX_W < MATRIX_W - 1: flag = True
		else: flag = False
	elif move_direction == 'up':
		if idx > MATRIX_W - 1: flag = True
		else: flag = False
	elif move_direction == 'down':
		if idx < MATRIX_SIZE - MATRIX_W: flag = True
		else: flag = False
	return flag

def RefreshBoard(psnake, pfood, pboard):
	temp_board = pboard[:]
	pfood_idx = pfood['x'] + pfood['y'] * MATRIX_W
	queue = []
	queue.append(pfood_idx)
	inqueue = [0] * MATRIX_SIZE
	found = False
	while len(queue) != 0:
		idx = queue.pop(0)
		if inqueue[idx] == 1:
			continue
		inqueue[idx] = 1
		for move_direction in ['left', 'right', 'up', 'down']:
			if isMovePossible(idx, move_direction):
				if (idx + MOVEDIRECTIONS[move_direction]) == (psnake[HEADINDEX]['x'] + psnake[HEADINDEX]['y'] * MATRIX_W):
					found = True
				if temp_board[idx + MOVEDIRECTIONS[move_direction]] < SNAKENUM:
					if temp_board[idx + MOVEDIRECTIONS[move_direction]] > temp_board[idx]+1:
						temp_board[idx + MOVEDIRECTIONS[move_direction]] = temp_board[idx] + 1
					if inqueue[idx + MOVEDIRECTIONS[move_direction]] == 0:
						queue.append(idx + MOVEDIRECTIONS[move_direction])
	return (found, temp_board)

def chooseShortestSafeMove(psnake, pboard):
	BESTMOVE = ERR
	min_distance = SNAKENUM
	for move_direction in ['left', 'right', 'up', 'down']:
		idx = psnake[HEADINDEX]['x'] + psnake[HEADINDEX]['y'] * MATRIX_W
		if isMovePossible(idx, move_direction) and (pboard[idx + MOVEDIRECTIONS[move_direction]] < min_distance):
			min_distance = pboard[idx + MOVEDIRECTIONS[move_direction]]
			BESTMOVE = move_direction
	return BESTMOVE

def findSnakeHead(snake_coords, direction):
	if direction == 'up':
		new_head = {'x': snake_coords[HEADINDEX]['x'],
					'y': snake_coords[HEADINDEX]['y'] - 1}
	elif direction == 'down':
		new_head = {'x': snake_coords[HEADINDEX]['x'],
					'y': snake_coords[HEADINDEX]['y'] + 1}
	elif direction == 'left':
		new_head = {'x': snake_coords[HEADINDEX]['x'] - 1,
					'y': snake_coords[HEADINDEX]['y']}
	elif direction == 'right':
		new_head = {'x': snake_coords[HEADINDEX]['x'] + 1,
					'y': snake_coords[HEADINDEX]['y']}
	return new_head

def virtualMove(psnake, pboard, pfood):
	temp_snake = psnake[:]
	temp_board = pboard[:]
	reset_tboard = ResetBoard(temp_snake, temp_board, pfood)
	temp_board = reset_tboard
	food_eated = False
	while not food_eated:
		refresh_tboard = RefreshBoard(temp_snake, pfood, temp_board)[1]
		temp_board = refresh_tboard
		move_direction = chooseShortestSafeMove(temp_snake, temp_board)
		snake_coords = temp_snake[:]
		temp_snake.insert(0, findSnakeHead(snake_coords, move_direction))
		if temp_snake[HEADINDEX] == pfood:
			reset_tboard = ResetBoard(temp_snake, temp_board, pfood)
			temp_board = reset_tboard
			pfood_idx = pfood['x'] + pfood['y'] * MATRIX_W
			temp_board[pfood_idx] = SNAKENUM
			food_eated = True
		else:
			new_head_idx = temp_snake[0]['x'] + temp_snake[0]['y'] * MATRIX_W
			temp_board[new_head_idx] = SNAKENUM
			end_idx = temp_snake[-1]['x'] + temp_snake[-1]['y'] * MATRIX_W
			temp_board[end_idx] = SPACENUM
			del temp_snake[-1]
	return temp_snake, temp_board

def isTailInside(psnake, pboard, pfood):
	temp_board = pboard[:]
	temp_snake = psnake[:]
	end_idx = temp_snake[-1]['x'] + temp_snake[-1]['y'] * MATRIX_W
	temp_board[end_idx] = FOODNUM
	v_food = temp_snake[-1]
	pfood_idx = pfood['x'] + pfood['y'] * MATRIX_W
	temp_board[pfood_idx] = SNAKENUM
	result, refresh_tboard = RefreshBoard(temp_snake, v_food, temp_board)
	temp_board = refresh_tboard
	for move_direction in ['left', 'right', 'up', 'down']:
		idx = temp_snake[HEADINDEX]['x'] + temp_snake[HEADINDEX]['y'] * MATRIX_W
		end_idx = temp_snake[-1]['x'] + temp_snake[-1]['y'] * MATRIX_W
		if isMovePossible(idx, move_direction) and (idx + MOVEDIRECTIONS[move_direction] == end_idx) and (len(temp_snake) > 3):
			result = False
	return result

def chooseLongestSafeMove(psnake, pboard):
	BESTMOVE = ERR
	max_distance = -1
	for move_direction in ['left', 'right', 'up', 'down']:
		idx = psnake[HEADINDEX]['x'] + psnake[HEADINDEX]['y'] * MATRIX_W
		if isMovePossible(idx, move_direction) and (pboard[idx + MOVEDIRECTIONS[move_direction]] > max_distance) and (pboard[idx + MOVEDIRECTIONS[move_direction]] < SPACENUM):
			max_distance = pboard[idx + MOVEDIRECTIONS[move_direction]]
			BESTMOVE = move_direction
	return BESTMOVE

def followTail(psnake, pboard, pfood):
	temp_snake = psnake[:]
	temp_board = ResetBoard(temp_snake, pboard, pfood)
	end_idx = temp_snake[-1]['x'] + temp_snake[-1]['y'] * MATRIX_W
	temp_board[end_idx] = FOODNUM
	v_food = temp_snake[-1]
	pfood_idx = pfood['x'] + pfood['y'] * MATRIX_W
	temp_board[pfood_idx] = SNAKENUM
	result, refresh_tboard = RefreshBoard(temp_snake, v_food, temp_board)
	temp_board = refresh_tboard
	temp_board[end_idx] = SNAKENUM
	# temp_board[pfood_idx] = FOOD
	return chooseLongestSafeMove(temp_snake, temp_board)

def findSafeWay(psnake, pboard, pfood):
	safe_move = ERR
	real_snake = psnake[:]
	real_board = pboard[:]
	v_psnake, v_pboard = virtualMove(psnake, pboard, pfood)
	if isTailInside(v_psnake, v_pboard, pfood):
		safe_move = chooseShortestSafeMove(real_snake, real_board)
	else:
		safe_move = followTail(real_snake, real_board, pfood)
	return safe_move

def anyPossibleMove(psnake, pboard, pfood):
	BESTMOVE = ERR
	reset_board = ResetBoard(psnake, pboard, pfood)
	pboard = reset_board
	result, refresh_board = RefreshBoard(psnake, pfood, pboard)
	pboard = refresh_board
	min_distance = SNAKENUM
	for move_direction in ['left', 'right', 'up', 'down']:
		idx = psnake[HEADINDEX]['x'] + psnake[HEADINDEX]['y'] * MATRIX_W
		if isMovePossible(idx, move_direction) and (pboard[idx + MOVEDIRECTIONS[move_direction]]<min_distance):
			min_distance = pboard[idx + MOVEDIRECTIONS[move_direction]]
			BESTMOVE = move_direction
	return BESTMOVE

def RunGame():
	board = [0] * MATRIX_SIZE
	start_x = random.randint(5, MATRIX_W-6)
	start_y = random.randint(5, MATRIX_H-6)
	snake_coords = [{'x': start_x, 'y': start_y},
					{'x': start_x-1, 'y': start_y},
					{'x': start_x-2, 'y': start_y}]
	apple_location = GetAppleLocation(snake_coords)
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				CloseGame()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					CloseGame()
		screen.fill(BGCOLOR)
		drawGrid()
		ShowSnake(snake_coords)
		ShowApple(apple_location)
		ShowScore(len(snake_coords) - 3)
		reset_board = ResetBoard(snake_coords, board, apple_location)
		board = reset_board
		result, refresh_board = RefreshBoard(snake_coords, apple_location, board)
		board = refresh_board
		if result:
			BESTMOVE = findSafeWay(snake_coords, board, apple_location)
		else:
			BESTMOVE = followTail(snake_coords, board, apple_location)
		if BESTMOVE == ERR:
			BESTMOVE = anyPossibleMove(snake_coords, board, apple_location)
		if BESTMOVE != ERR:
			new_head = findSnakeHead(snake_coords, BESTMOVE)
			snake_coords.insert(0, new_head)
			head_idx = snake_coords[HEADINDEX]['x'] + snake_coords[HEADINDEX]['y'] * MATRIX_W
			end_idx = snake_coords[-1]['x'] + snake_coords[-1]['y'] * MATRIX_W
			if (snake_coords[HEADINDEX]['x'] == apple_location['x']) and (snake_coords[HEADINDEX]['y'] == apple_location['y']):
				board[head_idx] = SNAKENUM
				if len(snake_coords) < MATRIX_SIZE:
					apple_location = GetAppleLocation(snake_coords)
			else:
				board[head_idx] = SNAKENUM
				board[end_idx] = SPACENUM
				del snake_coords[-1]
		else:
			return
		pygame.display.update()
		clock.tick(FPS)

def main():
	global screen, default_font, clock
	pygame.init()
	screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
	pygame.display.set_caption('AI Snake')
	default_font = pygame.font.Font('simkai.ttf', 18)
	clock = pygame.time.Clock()
	while True:
		RunGame()
		ShowEndInterface()

'''run'''
if __name__ == '__main__':
	main()