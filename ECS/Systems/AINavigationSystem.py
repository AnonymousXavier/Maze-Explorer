from ECS.Components import AIStateComponent, PathFindingComponent, PlayerInputTag, SpacialComponent
from ECS.Systems import PathFindingSystem
from Globals import Enums

pathfinding_entities = set()

def process(world: dict, spatial_grid: dict, events: list):
	for event in events:
		if event["type"] == Enums.EventType.PATHFIND_INTENT:
			obj_id = event["entity_id"]
			target_id = event["target_id"]
			path = PathFindingSystem.get_path_to_obj(world, spatial_grid, obj_id, target_id)
			world[obj_id][PathFindingComponent].path = path

			pathfinding_entities.add(obj_id)

	# NAVIGATION
	entities_done_pathfinding = []
	for obj_id in pathfinding_entities:
		path = world[obj_id][PathFindingComponent].path
		if len(path) > 0:
			px, py = world[obj_id][SpacialComponent].grid_pos
			nx, ny = path[0]

			dx, dy = nx - px, ny - py
			if dx == 0 and dy == 0:
				path.pop(0)
			else:
				world[obj_id][AIStateComponent].state = Enums.AI_STATES.MOVE
				movement_event = {"type": Enums.EventType.MOVEMENT_INTENT, "entity_id": obj_id, "dx": dx, "dy": dy}
				events.append(movement_event)
		else:
			entities_done_pathfinding.append(obj_id)
			world[obj_id][AIStateComponent].state = Enums.AI_STATES.SEARCH

	entity_that_found_player = None
	for obj_id in entities_done_pathfinding:
		# Before Removing.. find out if player an guard share the same location
		grid_pos = world[obj_id][SpacialComponent].grid_pos
		for entity_id in spatial_grid[grid_pos]:
			if PlayerInputTag in world[entity_id]:
				entity_that_found_player = obj_id
				break

		pathfinding_entities.remove(obj_id)

	return entity_that_found_player




