from Globals import Enums, Misc
from ECS.Components import InteractableComponent, SpacialComponent

interaction_occured = False

def process(world: dict, spatial_grid: dict, events: list):
	global interaction_occured
	for event in events:
		if event["type"] == Enums.EventType.INTERACTION_INTENT:
			interactor_id = event["entity_id"]

			grid_pos = world[interactor_id][SpacialComponent].grid_pos
			entities_id_sharing_that_position = spatial_grid[grid_pos]
			entities_sharing_that_position = [(entity_id, world[entity_id]) for entity_id in entities_id_sharing_that_position]

			for entity_id, entity in entities_sharing_that_position:
				if InteractableComponent in entity:
					if entity[InteractableComponent].action() and entity[InteractableComponent].one_time:
						Misc.remove_entity_from_grid(entity_id, grid_pos, spatial_grid)
						interaction_occured = True
