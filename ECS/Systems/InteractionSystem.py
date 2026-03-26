from Core import States
from Globals import Enums, Misc
from ECS.Components import ArtifactTag, ExtractionTag, InteractionComponent, PlayerInputTag, SpacialComponent


def process(world: dict, spatial_grid: dict, events: list):
	for event in events:
		if event["type"] == Enums.EventType.INTERACTION_INTENT:
			player_id = event["entity_id"]
			player = world[player_id]

			grid_pos = world[player_id][SpacialComponent].grid_pos
			entities_id_sharing_that_position = spatial_grid[grid_pos]
			entities_sharing_that_position = [(entity_id, world[entity_id]) for entity_id in entities_id_sharing_that_position]

			for entity_id, entity in entities_sharing_that_position:
				if InteractionComponent in entity:
					if PlayerInputTag not in entity:
						if ArtifactTag in entity:
							States.TAKEN_ARTIFACT = True
						elif ExtractionTag in entity:
							if States.TAKEN_ARTIFACT:
								print("Game Completed")
							else:
								print("Steal Artiface, we're waiting for you")

						

					if player[InteractionComponent].one_time:
						Misc.remove_entity_from_grid(player_id, grid_pos, spatial_grid)
					if entity[InteractionComponent].one_time:
						Misc.remove_entity_from_grid(entity_id, grid_pos, spatial_grid)
