import pygame, sys
import time
from Sudoku_Solver import is_valid, solve
from settings import *

class SudokuApp:
	def __init__(self):
		pygame.init()
		self.window = pygame.display.set_mode((WIDTH, HEIGHT))
		self.running = True
		self.mouse_pos = None
		self.selected = None
		self.model = INPUT_BOARD
		self.key = None
		self.temp = None
		self.locked_cubes = []
		self.buttons = []
		self.valid_input = True
		self.font = pygame.font.SysFont("arial", CUBE_SIZE//2)

	def run(self):
		start_timer = time.time()
		self.load_buttons()
		self.load_locked_cubes()
		while self.running:
			self.timer = round(time.time() - start_timer)
			self.events()
			self.update()
			self.draw()
		pygame.quit()
		sys.exit()

	def events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				self.selected = self.cube_coordinate()
				if self.buttons[0].update_button(self.mouse_pos):
					solve(self.model)
				if self.buttons[1].update_button(self.mouse_pos):
					self.reset_board()
			if self.selected != None and self.selected not in self.locked_cubes:
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_1 or event.key == pygame.K_KP1:
						self.key = 1
					if event.key == pygame.K_2 or event.key == pygame.K_KP2:
						self.key = 2
					if event.key == pygame.K_3 or event.key == pygame.K_KP3:
						self.key = 3
					if event.key == pygame.K_4 or event.key == pygame.K_KP4:
						self.key = 4
					if event.key == pygame.K_5 or event.key == pygame.K_KP5:
						self.key = 5
					if event.key == pygame.K_6 or event.key == pygame.K_KP6:
						self.key = 6
					if event.key == pygame.K_7 or event.key == pygame.K_KP7:
						self.key = 7
					if event.key == pygame.K_8 or event.key == pygame.K_KP8:
						self.key = 8
					if event.key == pygame.K_9 or event.key == pygame.K_KP9:
						self.key = 9
					if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE or event.key == pygame.K_KP0:
						self.key = 0
						self.update_board(self.key)
					self.temp = self.key
					if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
						self.temp = None
						self.update_board(self.key)


	def update_board(self, key):
		if is_valid(self.model, key, self.selected) or key == 0:
			self.valid_input = True
			self.model[self.selected[0]][self.selected[1]] = key
		else:
			self.valid_input = False

	def reset_board(self):
		for i in range(9):
			for j in range(9):
				if not (i,j) in self.locked_cubes:
					self.model[i][j] = 0


	def update(self):
		self.mouse_pos= pygame.mouse.get_pos()
		for button in self.buttons:
			button.update_button(self.mouse_pos)


	def draw(self):
		self.window.fill(WHITE)
		for button in self.buttons:
			button.draw_button(self.window)
		if self.selected:   self.draw_selection_box(self.selected)
		self.draw_locked_cubes(self.locked_cubes)
		self.draw_numbers(self.window)
		self.draw_grid()
		self.extra_func(self.window)
		pygame.display.update()

############ Helper Functions ##############

	def cube_coordinate(self):
		if self.mouse_pos[0] < GRID_POSITION[0] or self.mouse_pos[0] > GRID_POSITION[0] + GRID_WIDTH or self.mouse_pos[1] < GRID_POSITION[1] or self.mouse_pos[1] > GRID_POSITION[1] + GRID_HEIGHT:
			return None
		else:
			return ((self.mouse_pos[1] - GRID_POSITION[1]) // CUBE_SIZE, (self.mouse_pos[0] - GRID_POSITION[0]) // CUBE_SIZE)

	def draw_selection_box(self, pos):
		pygame.draw.rect(self.window, LIGHT_BLUE, (GRID_POSITION[0] + (pos[1] * CUBE_SIZE), GRID_POSITION[1] + (pos[0] * CUBE_SIZE), CUBE_SIZE, CUBE_SIZE))


	def draw_grid(self):
		pygame.draw.rect(self.window, BLACK, (GRID_POSITION[0], GRID_POSITION[1], GRID_WIDTH, GRID_HEIGHT), 3)
		for i in range(1,9):
			pygame.draw.line(self.window, BLACK, (GRID_POSITION[0], GRID_POSITION[1] + (i * CUBE_SIZE)), (GRID_POSITION[0] + GRID_WIDTH, GRID_POSITION[1] + (i * CUBE_SIZE)), 3 if i % 3 == 0 else 1)
			pygame.draw.line(self.window, BLACK, (GRID_POSITION[0] + (i * CUBE_SIZE), GRID_POSITION[1]), (GRID_POSITION[0] + (i * CUBE_SIZE), GRID_POSITION[1] + GRID_HEIGHT), 3 if i % 3 == 0 else 1)


	def draw_locked_cubes(self, locked):
		for cube in locked:
			pygame.draw.rect(self.window, GREY, (cube[1]*CUBE_SIZE+GRID_POSITION[0], cube[0]*CUBE_SIZE+GRID_POSITION[1], CUBE_SIZE, CUBE_SIZE))

	
	def draw_numbers(self, window):
		if self.temp:
			self.text_to_screen(window, self.temp, [self.selected[1]*CUBE_SIZE+GRID_POSITION[0], self.selected[0]*CUBE_SIZE+GRID_POSITION[1]])
		for row in range(9):
			for col in range(9):
				if self.model[row][col] != 0:
					pos = [GRID_POSITION[0] + (col * CUBE_SIZE), GRID_POSITION[1] + (row * CUBE_SIZE)]
					self.text_to_screen(window, self.model[row][col], pos)


	def text_to_screen(self, window, text, pos):
		font = self.font.render(str(text), 1, BLACK)
		font_width = font.get_width()
		font_height = font.get_height()
		pos[0] += (CUBE_SIZE - font_width)//2
		pos[1] += (CUBE_SIZE - font_height)//2
		window.blit(font, pos)

	# Getting the position of all the initial values in the board
	def load_locked_cubes(self):
		for row in range(9):
			for col in range(9):
				if self.model[row][col] != 0:
					self.locked_cubes.append((row,col))


	def load_buttons(self):
		solve_button = Button(205, 10, 80, 30, "SOLVE")
		self.buttons.append(solve_button)
		reset_button = Button(290, 10, 80, 30, "RESET")
		self.buttons.append(reset_button)


	def is_finished(self):
		for i in range(9):
			for j in range(9):
				if self.model[i][j] == 0:
					return False
		return True


	def extra_func(self, window):
		if self.is_finished():
			font = pygame.font.SysFont("arial", 30)
			text = font.render("GAME OVER", 1, BLACK)
			text_height = text.get_height()
			window.blit(text, (GRID_POSITION[0], GRID_POSITION[1] - GRID_POSITION[0] - text_height))

		# Display invalid text if user enters invalid input
		font = pygame.font.SysFont("arial", 20)
		if not self.valid_input:
			invalid_text = font.render("INVALID", 1, BLACK)
			invalid_text_height = invalid_text.get_height()
			window.blit(invalid_text, (GRID_POSITION[0], GRID_POSITION[1] - GRID_POSITION[0] - invalid_text_height))

		# Display timer
		timer_text = font.render("Time: " + self.format_time(self.timer), 1, BLACK)
		timer_font_width = timer_text.get_width()
		timer_font_height = timer_text.get_height()
		window.blit(timer_text, (WIDTH-GRID_POSITION[0]-timer_font_width ,GRID_POSITION[1]-timer_font_height - GRID_POSITION[0]))

	# Convert time into minute:sec format
	def format_time(self, secs):
	    sec = secs%60
	    minute = secs//60
	    hour = minute//60
	    mat = " " + str(minute) + ":" + str(sec)
	    return mat


class Button:
	def __init__(self, x, y, width, height, text=None, color=(73,73,73), highlighted_color=(189,189,189)):
		self.image = pygame.Surface((width, height))
		self.pos = (x, y)
		self.rect = self.image.get_rect()
		self.rect.topleft = self.pos
		self.text = text
		self.color = color
		self.highlighted_color = highlighted_color
		self.higlighted = False

	def update_button(self, mouse):
		self.higlighted = True if self.rect.collidepoint(mouse) else False
		return self.higlighted

	def draw_button(self, window):
		self.image.fill(self.highlighted_color if self.higlighted else self.color)
		window.blit(self.image, self.pos)
		font = pygame.font.SysFont("arial", 20)
		font_text = font.render(self.text, 1, WHITE)
		window.blit(font_text, (self.pos[0]+12, self.pos[1]+2))

