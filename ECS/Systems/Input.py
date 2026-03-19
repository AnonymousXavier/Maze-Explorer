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

	pressed_keys = pygame.key.get_pressed()
	# Handle Player Movements

	if player_id:
		if is_key_pressed(pressed_keys, Settings.CONTROLS.DOWN): 
			global_event.append({"type": Enums.EventType.MOVEMENT_INTENT, "entity_id": player_id, "dx": 0, "dy": 1})
		if is_key_pressed(pressed_keys,Settings.CONTROLS.UP): 
			global_event.append({"type": Enums.EventType.MOVEMENT_INTENT, "entity_id": player_id, "dx": 0, "dy": -1})
		if is_key_pressed(pressed_keys, Settings.CONTROLS.LEFT): 
			global_event.append({"type": Enums.EventType.MOVEMENT_INTENT, "entity_id": player_id, "dx": -1, "dy": 0})
		if is_key_pressed(pressed_keys, Settings.CONTROLS.RIGHT): 
			global_event.append({"type": Enums.EventType.MOVEMENT_INTENT, "entity_id": player_id, "dx": 1, "dy": 0})

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			States.GAME_RUNNING = False

def is_key_pressed(pressed_keys, binded_keys: tuple):
	for key in binded_keys:
		if pressed_keys[key]:
			return True
	return False