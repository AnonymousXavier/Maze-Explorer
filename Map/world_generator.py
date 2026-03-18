import pygame
from Map.maze_generator import maze_generator
from Globals import Settings, Enums

class world_generator:
	def __init__(self) -> None:
		self.maze_gen = maze_generator()
		self.map = self.create_map()

	def build(self):
		print("Generating Grid")
		self.maze_gen.generate()
		print("Generated Grid")
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

	def create_map(self):
		map_dict = {}
		for y in range(Settings.MAP.WORLD_HEIGHT):
			for x in range(Settings.MAP.WORLD_WIDTH):
				map_dict[(x, y)] = Enums.CELL_ELEMENTS.EMPTY

		return map_dict

	def scale_grid_cells_to_rooms(self):
		rw, rh = Settings.MAP.ROOM_WIDTH, Settings.MAP.ROOM_HEIGHT
		hrw, hrh = rw // 2, rh // 2

		for (xi, yi) in self.maze_gen.grid:
			# Get map eqivalent of maze cell - topleft position
			x = xi * rw
			y = yi * rh

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
				nx = cx + dx * hrw
				ny = cy + dy * hrh

				self.map[(nx, ny)] = Enums.CELL_ELEMENTS.DOOR
