from math import cos, sin, radians

from ECS import Factories
from ECS.Components import RayCastComponent, RayCastRegion, SpacialComponent, ObstacleTag
from Globals import Misc, Enums

def process(world: dict, spatial_grid: dict, events: list):
	for event in events:
		obj_id = event["entity_id"]
		obj = world[obj_id]
		if event["type"] == Enums.EventType.SEARCH_INTENT:
			if RayCastComponent in obj and SpacialComponent in obj:

				facing_direction = event["direction"]
				obj[RayCastRegion] = RayCastRegion()
				obj[RayCastComponent].facing_direction = facing_direction
				cast_ray_and_spawn_in_grid(world, spatial_grid, obj)

			
def cast_ray_and_spawn_in_grid(world: dict, spatial_grid: dict, obj: dict):
	facing_direction = obj[RayCastComponent].facing_direction
	angle_spread = obj[RayCastComponent].angle_spread

	pxi, pyi = obj[SpacialComponent].grid_pos

	length = obj[RayCastComponent].length

	min_angle = facing_direction % 360 - angle_spread // 2
	max_angle = facing_direction % 360 + angle_spread // 2

	# Add Rays
	for angle in range(min_angle, max_angle + 1):
		arc_length = 0
		hit_a_wall = False

		while arc_length < length + 1:
			xi = round(cos(radians(angle)) * arc_length)
			yi = round(sin(radians(angle)) * arc_length)
			ray_pos = pxi + xi, pyi + yi

			if ray_pos in spatial_grid:
				for _obj_id in spatial_grid[ray_pos]:
					if ObstacleTag in world[_obj_id]:
						hit_a_wall = True
          	
			if hit_a_wall: break

			obj[RayCastRegion].points.add(ray_pos)

			arc_length += 0.2
