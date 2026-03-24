from Globals import Enums, Settings

def register_entity_in_grid(entity_id: int, pos: tuple, spatial_grid: dict):
	if pos not in spatial_grid:
		spatial_grid[pos] = [entity_id]
	else:
		spatial_grid[pos].append(entity_id)

def remove_entity_from_grid(entity_id: int, pos: tuple, spatial_grid: dict):
	if pos in spatial_grid:
		if entity_id in spatial_grid[pos]:
			spatial_grid[pos].remove(entity_id)
			if spatial_grid[pos] == []:
				del spatial_grid[pos]
			return True

def fetch_entities_from_grid(pos: tuple, spatial_grid: dict):
	if pos in spatial_grid:
		return spatial_grid[pos]

def interpolate_towards(position: tuple, target_position, speed: float, interpolation_type=Enums.INTERPOLATION.LINEAR):
	tx, ty = target_position
	px, py = position

	match interpolation_type:
		case Enums.INTERPOLATION.EASE_OUT:
			speed = speed * (2 - speed)

	return lerp(px, tx, speed), lerp(py, ty, speed)

def move_towards(position: tuple, target_position: tuple, speed: float):
	px, py = position
	tx, ty = target_position
	dx, dy = round(tx - px), round(ty - py)

	nx, ny = px + dx * speed, py + dy * speed

	if dx == 0:
		nx = tx
	if dy == 0:
		ny = ty

	return nx, ny


def lerp(start: float, end: float, speed: float):
	if abs(speed) > abs(round(end - start)): return end
	return start + round(end - start) * speed

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

def get_half_size_of_room():
	rw, rh = Settings.MAP.ROOM_WIDTH, Settings.MAP.ROOM_HEIGHT

	hrw = 0
	hrh = 0

	if rw % 2 == 0 and rh % 2 == 0:
		hrw = round(rw / 2) - 1
		hrh = round(rh / 2) - 1
	else:
		hrw = rw // 2 
		hrh = rh // 2

	print(hrw, hrh)
	return hrw, hrh

def clamp(value, min_value, max_value):
	if value > max_value:
		return min_value
	if value < min_value:
		return max_value
	return value