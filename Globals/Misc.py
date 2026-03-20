import pygame

from Globals import Enums

def register_entity_in_grid(entity_id: int, pos: tuple, spatial_grid: dict):
	if pos not in spatial_grid:
		spatial_grid[pos] = [entity_id]
	else:
		spatial_grid[pos].append(entity_id)

def remove_entity_from_grid(entity_id: int, pos: tuple, spatial_grid: dict):
	if entity_id in spatial_grid[pos]:
		spatial_grid[pos].remove(entity_id)
		if spatial_grid[pos] == []:
			del spatial_grid[pos]
		return True

def interpolate_towards(position: tuple, target_position, speed: float, interpolation_type=Enums.INTERPOLATION.LINEAR):
	tx, ty = target_position
	px, py = position

	match interpolation_type:
		case Enums.INTERPOLATION.EASE_OUT:
			speed = speed * (2 - speed)

	return lerp(px, tx, speed), lerp(py, ty, speed)

def move_towards(position: tuple, target_position: tuple, speed: float):
	negligible_distance = 0.01

	px, py = position
	tx, ty = target_position
	dx, dy = tx - px, ty - py

	sx, sy = min(abs(speed), abs(dx)), min(abs(speed), abs(dy))

	nx, ny = px + dx * sx, py + dy * sy
	if abs(sx) < negligible_distance:
		nx = tx
	if abs(sy) < negligible_distance:
		ny = ty

	return nx, ny


def lerp(start: float, end: float, speed: float):
	if abs(speed) > abs(end - start): return end
	return start + (end - start) * speed

def get_visible_entities_with(world: dict, spatial_grid: dict, cam_boundary: dict, *components):
	
	cam_left, cam_top = cam_boundary["left"], cam_boundary["top"]
	cam_right, cam_bottom = cam_boundary["right"], cam_boundary["bottom"]

	visible_renderable_entities = []
	for iy in range(cam_top, cam_bottom + 1):
		for ix in range(cam_left, cam_right + 1):
			if (ix, iy) in spatial_grid:
				for obj_id in spatial_grid[(ix, iy)]:
					is_valid = True
					# Add object if it has all the properties
					for component in components:
						if component not in world[obj_id]: 
							is_valid = False
							break
					if is_valid:
						visible_renderable_entities.append(obj_id)

	return visible_renderable_entities
