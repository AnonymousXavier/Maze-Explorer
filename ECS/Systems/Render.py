from ECS.Components import SpacialComponent, RenderComponent

import pygame

def process(surface: pygame.Surface, world: dict):
	for obj_id in world:
		if RenderComponent in world[obj_id] and SpacialComponent in world[obj_id]:
			obj = world[obj_id]
			pygame.draw.rect(surface, obj[RenderComponent].color, obj[SpacialComponent].rect)