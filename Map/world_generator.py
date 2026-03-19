import pygame
from Map.maze_generator import maze_generator
from Globals import Settings, Enums

class world_generator:
	def __init__(self) -> None:
		self.maze_gen = maze_generator()
		self.map = {}

		self.start_pos: tuple
		self.stop_pos: tuple

	def build(self):
		print("Generating Grid")
		self.maze_gen.generate()

		self.stop_pos = self.maze_gen.stop_pos
		self.start_pos = self.maze_gen.start_pos

		print("Expanding Grid to Rooms")
		self.scale_grid_cells_to_rooms()
		print("Build Complete")


	def draw(self, surface: pygame.Surface):
		self.draw_map(surface)

	def draw_map(self, surface: pygame.Surface):
		r = Settings.MAP.GRID_ROWS
		c = Settings.MAP.GRID_COLS
		cs = (Settings.WINDOW.WIDTH / c) * Settings.MAP.SPACING_TO_WIDTH_RATIO
		cw, ch = (Settings.WINDOW.WIDTH / c) - cs, (Settings.WINDOW.HEIGHT / r) - cs

		start_xi, start_yi = self.start_pos
		stop_xi, stop_yi = self.stop_pos

		for (xi, yi) in self.map:
			x = xi * (cw + cs)
			y = yi * (ch + cs)

			col = Settings.COLOURS.BLUE
			if self.map[(xi, yi)] == Enums.CELL_ELEMENTS.WALL:
				col = Settings.COLOURS.GREY
			elif self.map[(xi, yi)] == Enums.CELL_ELEMENTS.DOOR:
				col = Settings.COLOURS.GREEN

			rect = pygame.Rect(x, y, cw, ch)
			pygame.draw.rect(surface, col, rect)

		start_x, start_y = start_xi * (cw + cs), start_yi * (ch + cs)
		stop_x, stop_y = stop_xi * (cw + cs), stop_yi * (ch + cs)

		start_rect = pygame.Rect(start_x, start_y, cw, ch)
		stop_rect = pygame.Rect(stop_x, stop_y, cw, ch)

		pygame.draw.rect(surface, Settings.COLOURS.BLUE, start_rect)
		pygame.draw.rect(surface, Settings.COLOURS.RED, stop_rect)

	def scale_grid_cells_to_rooms(self):
		rw, rh = Settings.MAP.ROOM_WIDTH, Settings.MAP.ROOM_HEIGHT

		hrw = round(rw / 2) - 1
		hrh = round(rh / 2) - 1

		for (yi, xi) in self.maze_gen.grid:
			# Get map eqivalent of maze cell - topleft position
			x = xi * (rw - 1)
			y = yi * (rh - 1)

			# Ganerate Walls for the rooms
			for ryi in range(rw):
				for rxi in range(rh):
					if rxi == 0 or ryi == 0 or rxi == rw - 1 or ryi == rh - 1:
						self.map[(x + rxi, y + ryi )] = Enums.CELL_ELEMENTS.WALL

			# Generate doors based on neighbours
			for (nxi, nyi) in self.maze_gen.grid[(xi, yi)]:

				dx = nxi - xi
				dy = nyi - yi

				cx, cy = x + hrw, y + hrh

				# add scaled displacement to rooms center
				if rw % 2 == 0 and rh % 2 == 0:
					# add scaled displacement to rooms center
					if dx < 0:
						nx = cx + dx * hrw
					else:
						nx = 1 + cx + dx * hrw

					if dy < 0:
						ny = cy + dy * hrh
					else:
						ny = 1 + cy + dy * hrh

					# # Expand Doors to be a bit wider
					self.map[(nx -abs(dy), ny -abs(dx))] = Enums.CELL_ELEMENTS.DOOR
				else:
					nx = cx + dx * hrw
					ny = cy + dy * hrh

					# # Expand Doors to be a bit wider
					self.map[(nx + dy, ny + dx)] = Enums.CELL_ELEMENTS.DOOR
					self.map[(nx - dy, ny - dx)] = Enums.CELL_ELEMENTS.DOOR

				self.map[(nx, ny)] = Enums.CELL_ELEMENTS.DOOR

		start_xi, start_yi = self.start_pos
		stop_xi, stop_yi = self.stop_pos

		start_xi, start_yi = start_xi * rw + hrw, start_yi * rh + hrh
		stop_xi, stop_yi = stop_xi * rw + hrw, stop_yi * rh + hrh

		self.start_pos = start_xi, start_yi
		self.stop_pos = stop_xi, stop_yi