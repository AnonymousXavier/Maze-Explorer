import pygame

from Core import States
from ECS.Components import PlayerInputTag
from Globals import Enums, Settings

def process(world: dict, global_event: list):
	player_id: int | None = None

	for obj_id in world:
		if PlayerInputTag in world[obj_id]:
			player_id = obj_id
			break

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			States.GAME_RUNNING = False

		# Handle Player Movements
		if player_id:
			if event.type == pygame.KEYDOWN:
				if event.key in Settings.CONTROLS.DOWN: 
					global_event.append({"type": Enums.EventType.MOVEMENT_INTENT, "entity_id": player_id, "dx": 0, "dy": 1})
				if event.key in Settings.CONTROLS.UP: 
					global_event.append({"type": Enums.EventType.MOVEMENT_INTENT, "entity_id": player_id, "dx": 0, "dy": -1})
				if event.key in Settings.CONTROLS.LEFT: 
					global_event.append({"type": Enums.EventType.MOVEMENT_INTENT, "entity_id": player_id, "dx": -1, "dy": 0})
				if event.key in Settings.CONTROLS.RIGHT: 
					global_event.append({"type": Enums.EventType.MOVEMENT_INTENT, "entity_id": player_id, "dx": 1, "dy": 0})