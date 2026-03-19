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

def move_towards(position: tuple, target_position, speed: float, interpolation_type=Enums.INTERPOLATION.LINEAR):
	tx, ty = target_position
	px, py = position

	match interpolation_type:
		case Enums.INTERPOLATION.EASE_OUT:
			speed = speed * (2 - speed)

	return lerp(px, tx, speed), lerp(py, ty, speed)

def lerp(start: float, end: float, speed: float):
	if abs(speed) > abs(end - start): return end
	return start + (end - start) * speed