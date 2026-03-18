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
