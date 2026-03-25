import random

from ECS import Factories
from Globals import Cache, Misc
from Map.maze_generator import maze_generator
from Map.world_generator import world_generator
from Globals import Enums, Settings

random.seed(Settings.MAP.SEED)

def build_level(world: dict, spatial_grid: dict):
	world_gen = world_generator()
	world_gen.build()

	spawn_walls(world, spatial_grid, world_gen)

	return world_gen.start_pos, world_gen.stop_pos

def spawn_walls(world: dict, spatial_grid: dict, world_gen):
	for (ix, iy) in world_gen.map:
		cell_id = world_gen.map[(ix, iy)]["cell_id"]
		if cell_id == Enums.CELL_ELEMENTS.EMPTY:
			continue

		sxi, syi =  world_gen.map[(ix, iy)]["sprite_id"]
		sprite = Cache.SPRITES.TILESET[syi][sxi]
		entity_id: int | None = None

		match cell_id:
			case Enums.CELL_ELEMENTS.WALL:
				entity_id = Factories.spawn_wall(world, spatial_grid, ix, iy, sprite)
			case Enums.CELL_ELEMENTS.DOOR:
				entity_id = Factories.spawn_door(world, spatial_grid, ix, iy, sprite)

		Misc.register_entity_in_grid(entity_id, (ix, iy), spatial_grid)

def spawn_guards(world: dict, spatial_grid: dict):
	rw, rh = Settings.MAP.ROOM_SIZE
	hrw, hrh = Misc.get_half_size_of_room()
	x_factor = rw - 1
	y_factor = rh - 1

	spawned_guards_positions = set()
	n = 0 # Spawned Guards Count

	while n < Settings.GAME.NUMBER_OF_GUARDS:
		xi, yi = random.randint(0, Settings.MAP.COLS - 1), random.randint(0, Settings.MAP.ROWS - 1)
		grid_x = xi * x_factor + hrw
		grid_y = yi * y_factor + hrh

		if (grid_x, grid_y) not in spawned_guards_positions:
			spawned_guards_positions.add((grid_x, grid_y))

			Factories.spawn_guard(world, spatial_grid, grid_x, grid_y)
			n += 1
