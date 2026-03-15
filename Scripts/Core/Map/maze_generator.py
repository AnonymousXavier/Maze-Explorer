import pygame
import random

from Scripts.Globals import Settings
random.seed(Settings.MAP.SEED)

class maze_generator:
	def __init__(self) -> None:
		self.grid: dict[tuple[int, int], list] = self.create_grid()

	def create_grid(self):
		grid = {}
		for y in range(Settings.MAP.ROWS):
			for x in range(Settings.MAP.COLS):
				grid[(x, y)] = []

		return grid

	def generate(self, start_pos=(0, 0)):
		path: list[tuple[int, int]] = [start_pos]
		current_pos = start_pos

		while True:
			neighbours = self.get_free_neighbours_of(current_pos)

			if len(path) == 0:
				break

			if neighbours == []:
				current_pos = path.pop()
				continue

			path.append(current_pos)

			next_pos = random.choice(neighbours)
			self.grid[current_pos].append(next_pos)
			self.grid[next_pos].append(current_pos)
			current_pos = next_pos

	def get_free_neighbours_of(self, pos: tuple[int, int]):
		px, py = pos
		directions = ( (1, 0), (-1, 0), (0, 1), (0, -1) )
		neighbours: list[tuple[int, int]] = []

		for (dx, dy) in directions:
			nx, ny = dx + px, dy + py
			if nx >= 0 and ny >= 0 and nx < Settings.MAP.COLS and ny < Settings.MAP.ROWS:
				if self.grid[(nx, ny)] == []:
					neighbours.append((nx, ny))

		return neighbours

	def debug_draw_path(self, surface: pygame.Surface):
		w, h = (Settings.MAP.CELL_WIDTH + Settings.MAP.CELL_SPACING), (Settings.MAP.CELL_HEIGHT + Settings.MAP.CELL_SPACING)

		for (xi, yi) in self.grid:
			x = xi * w
			y = yi * h

			rect = pygame.Rect(x, y, Settings.MAP.CELL_WIDTH, Settings.MAP.CELL_HEIGHT)

			for (nxi, nyi) in self.grid[(xi, yi)]:
				nx = nxi * w
				ny = nyi * h
				next_rect = pygame.Rect(nx, ny, Settings.MAP.CELL_WIDTH, Settings.MAP.CELL_HEIGHT)
				pygame.draw.line(surface, Settings.COLOURS.RED, rect.center, next_rect.center, width=10)