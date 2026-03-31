from math import cos, sin, radians
import pygame

from ECS.Components import PathFindingComponent, RayCastComponent, RayCastRegion, SpacialComponent, ObstacleTag, PlayerInputTag
from Globals import Enums, Misc, Settings

directions = {
    -90: (0, -1),
    0: (1, 0),
    90: (0, 1),
    180: (-1, 0),
}
frame = 0

ray_surface_size = -1, -1
found_player = False

def process(world: dict, spatial_grid: dict, events: list):
	global frame
	if frame % (Settings.WINDOW.FPS / Settings.UPDATE.RAYCASTS_PER_SEC) == 0:
		for event in events:
			obj_id = event["entity_id"]
			obj = world[obj_id]
			if event["type"] == Enums.EventType.SEARCH_INTENT:
				if RayCastComponent in obj and SpacialComponent in obj:

					facing_direction = event["direction"]
					obj[RayCastRegion] = RayCastRegion()
					obj[RayCastComponent].facing_direction = facing_direction
					cast_ray_and_spawn_in_grid(world, spatial_grid, obj)

	frame += 1

			
def cast_ray_and_spawn_in_grid(world: dict, spatial_grid: dict, obj: dict):
	facing_direction = obj[RayCastComponent].facing_direction
	angle_spread = obj[RayCastComponent].angle_spread

	sw, sh = Settings.SPRITES.SIZE
	px, py = obj[SpacialComponent].rect.center
	dx, dy = directions[facing_direction]
	pxi, pyi = (px // sw) + dx, (py // sh) + dy

	length = obj[RayCastComponent].length

	min_angle = facing_direction % 360 - angle_spread // 2
	max_angle = facing_direction % 360 + angle_spread // 2

	# CONE GENERATION CARIABLES
	cw, ch = int(2 * length * sw), int(2 * length * sh)
	cx, cy =  cw // 2,  ch // 2
	cone_surface = pygame.Surface((cw, ch), pygame.SRCALPHA)
	sx, sy = (cx, cy)
	cone_points = [(sx, sy)]

	is_pathfinding = len(obj[PathFindingComponent].path) > 0

	# Add Rays
	current_angle = min_angle
	while current_angle <= max_angle:
		arc_length = 0
		hit_a_wall = False

		if not is_pathfinding:
			# RAYCASTING
			while arc_length < length - 1:
				xi = round(cos(radians(current_angle)) * arc_length)
				yi = round(sin(radians(current_angle)) * arc_length)
				ray_pos = pxi + xi, pyi + yi

				if ray_pos in spatial_grid:
					for _obj_id in spatial_grid[ray_pos]:
						if ObstacleTag in world[_obj_id]:
							hit_a_wall = True
	          	
				if hit_a_wall: break

				obj[RayCastRegion].points.add(ray_pos)
				entities = Misc.fetch_entities_from_grid(ray_pos, spatial_grid)

				if entities:
					# For now add only if its a player
					for entity_id in entities:
						if PlayerInputTag in world[entity_id]:
							global found_player
							obj[RayCastRegion].found_entities.add(entity_id)
							found_player = True

				arc_length += 0.2

		# CONE GENERATION
		fxi = sx + round(cos(radians(current_angle)) * arc_length) * sw
		fyi = sy + round(sin(radians(current_angle)) * arc_length) * sh

		cone_points.append((fxi, fyi))

		current_angle += Settings.GAME.RAYCAST_SHAPE_ACCURACY
	pygame.draw.polygon(cone_surface, Settings.DEBUG.RAYCAST_COLOR, cone_points)

	obj[RayCastRegion].size = (cw, ch)
	obj[RayCastRegion].shape = cone_surface
	obj[RayCastRegion].pivot = px + dx * sw - cx, py + dy * sh - cy