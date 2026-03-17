import pygame

from Core import States
from ECS.Components import SpacialComponent, RenderComponent, PlayerInputTag
from Globals import Settings

def spawn_player(world: dict, x: int, y: int):
	new_id = States.NEXT_ENTITY_ID
	States.NEXT_ENTITY_ID += 1

	player = {
		SpacialComponent: SpacialComponent(
			rect=pygame.Rect(x, y, Settings.SPRITES.WIDTH, Settings.SPRITES.HEIGHT)
		),
		RenderComponent: RenderComponent(Settings.PLAYER_DEFAULTS.COLOR),
		PlayerInputTag: PlayerInputTag()
	}

	world[new_id] = player

	return new_id