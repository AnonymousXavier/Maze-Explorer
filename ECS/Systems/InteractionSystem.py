from Core import States
from Globals import Enums
from ECS.Components import InteractionComponent, SpacialComponent


def process(world: dict, spatial_grid: dict, events: list):
	for event in events:
		if event["type"] == Enums.EventType.INTERACTION_INTENT:
			obj_id = event["entity_id"]
			grid_pos = world[obj_id][SpacialComponent].grid_pos
			entities_id_sharing_that_position = spatial_grid[grid_pos]
			entities_sharing_that_position = [world[entity_id] for entity_id in entities_id_sharing_that_position]

			for entity in entities_sharing_that_position:
				if InteractionComponent in entity:
					if entity[InteractionComponent].layer == world[obj_id][InteractionComponent].mask:
						States.GAME_STATES[event["property"]] = event["set_to"]
