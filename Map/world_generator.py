import pygame
from Map.maze_generator import maze_generator
from Globals import Cache, Settings, Enums

class world_generator:
	def __init__(self) -> None:
		self.maze_gen = maze_generator()
		self.map = {}

		self.start_pos: tuple
		self.stop_pos: tuple

	def build(self):
		self.maze_gen.generate()
		self.scale_grid_cells_to_rooms()
		self.assign_sprite_to_map_cells()

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

		hrw = 0
		hrh = 0

		x_factor = rw - 1
		y_factor = rh - 1

		for (xi, yi) in self.maze_gen.grid:
			# Get map eqivalent of maze cell - topleft position
			x = xi * x_factor
			y = yi * y_factor

			# Ganerate Walls for the rooms
			for ryi in range(rw):
				for rxi in range(rh):
					if rxi == 0 or ryi == 0 or rxi == rw - 1 or ryi == rh - 1:
						self.map[(x + rxi, y + ryi )] = {"cell_id": Enums.CELL_ELEMENTS.WALL, "sprite_id": ""}

			# Generate doors based on neighbours
			for (nxi, nyi) in self.maze_gen.grid[(xi, yi)]:

				dx = nxi - xi
				dy = nyi - yi

				# add scaled displacement to rooms center
				if rw % 2 == 0 and rh % 2 == 0:
					hrw = round(rw / 2) - 1
					hrh = round(rh / 2) - 1

					cx, cy = x + hrw, y + hrh

					# add scaled displacement to rooms center
					if dx < 0:
						nx = cx + dx * hrw
					else:
						nx = 1 + cx + dx * hrw

					if dy < 0:
						ny = cy + dy * hrh
					else:
						ny = 1 + cy + dy * hrh

				else:
					hrw = rw // 2 
					hrh = rh // 2

					cx, cy = x + hrw, y + hrh

					nx = cx + dx * hrw
					ny = cy + dy * hrh

				self.map[(nx, ny)] = {"cell_id": Enums.CELL_ELEMENTS.DOOR, "sprite_id": ""}

		hrw = rw // 2 
		hrh = rh // 2

		start_xi, start_yi = self.maze_gen.start_pos
		stop_xi, stop_yi = self.maze_gen.stop_pos

		start_x, start_y = start_xi * x_factor + hrw, start_yi * x_factor + hrh
		stop_x, stop_y   = stop_xi  * x_factor + hrw, stop_yi  * x_factor + hrh

		self.start_pos = start_x, start_y
		self.stop_pos = stop_x, stop_y

	def assign_sprite_to_map_cells(self):
		for (xi, yi) in self.map:
			cell_id = (xi, yi)
			above_id = (xi, yi - 1)
			below_id = (xi, yi + 1)
			left_id  = (xi - 1, yi)
			right_id = (xi + 1, yi)

			cell_above = None if above_id not in self.map else self.map[above_id]
			cell_below = None if below_id not in self.map else self.map[below_id]
			cell_left  = None if left_id not in self.map else self.map[left_id]
			cell_right = None if right_id not in self.map else self.map[right_id]

			if self.map[cell_id]["cell_id"] == Enums.CELL_ELEMENTS.WALL:
				if cell_above and cell_left and cell_right and cell_below:
					self.map[cell_id]["sprite_id"] = Cache.tileset_dict["wall_tee_top_bottom_right_left"]
				elif cell_above and cell_left and cell_below:
					self.map[cell_id]["sprite_id"] = Cache.tileset_dict["wall_tee_top_bottom_left"]
				elif cell_above and cell_right and cell_below:
					self.map[cell_id]["sprite_id"] = Cache.tileset_dict["wall_tee_top_bottom_right"]
				elif cell_above and cell_left and cell_right:
					self.map[cell_id]["sprite_id"] = Cache.tileset_dict["wall_tee_top_right_left"]
				elif cell_left and cell_right and cell_below:
					self.map[cell_id]["sprite_id"] = Cache.tileset_dict["wall_tee_bottom_left_right"]

				elif cell_left and cell_above:
					self.map[cell_id]["sprite_id"] = Cache.tileset_dict["bottom_right_wall"]
				elif cell_right and cell_above:
					self.map[cell_id]["sprite_id"] = Cache.tileset_dict["bottom_left_wall"]
				elif cell_left and cell_below:
					self.map[cell_id]["sprite_id"] = Cache.tileset_dict["top_right_wall"]
				elif cell_right and cell_below:
					self.map[cell_id]["sprite_id"] = Cache.tileset_dict["top_left_wall"]

				elif cell_above and cell_below:
					self.map[cell_id]["sprite_id"] = Cache.tileset_dict["middle_left_wall"]

				elif cell_right and cell_left:
					self.map[cell_id]["sprite_id"] = Cache.tileset_dict["top_middle_wall"]

			if self.map[cell_id]["cell_id"] == Enums.CELL_ELEMENTS.DOOR:

				if cell_above and cell_below:
					self.map[cell_id]["sprite_id"] = Cache.tileset_dict["door_top_bottom"]
				elif cell_left and cell_right:
					self.map[cell_id]["sprite_id"] = Cache.tileset_dict["door_left_right"]

