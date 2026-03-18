from ECS import Factories
from Globals import Misc
from Map.world_generator import world_generator
from Globals import Enums


def build_level(world: dict, spatial_grid: dict):
	world_gen = world_generator()
	world_gen.build()

	for (ix, iy) in world_gen.map:
		cell_id = world_gen.map[(ix, iy)]
		entity_id: int | None = None

		match cell_id:
			case Enums.CELL_ELEMENTS.EMPTY:
				continue
			case Enums.CELL_ELEMENTS.WALL:
				entity_id = Factories.spawn_wall(world, spatial_grid, ix, iy)
			case Enums.CELL_ELEMENTS.DOOR:
				entity_id = Factories.spawn_door(world, spatial_grid, ix, iy)

		# print(entity_id, cell_id)
		Misc.register_entity_in_grid(entity_id, (ix, iy), spatial_grid)

