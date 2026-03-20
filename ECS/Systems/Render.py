from ECS.Components import SpacialComponent, RenderComponent
from ECS.Systems import CameraSystem

import pygame

from Globals import Misc, Settings

def process(surface: pygame.Surface, world: dict, spatial_grid: dict, camera:dict):
	camera_rect: pygame.Rect = camera[SpacialComponent].rect

	cam_boundary = CameraSystem.get_boundary_of(camera)
	visible_renderable_entities = Misc.get_visible_entities_with(world, spatial_grid, cam_boundary, RenderComponent)

	sorted_entities = sorted(
		visible_renderable_entities,
		key=lambda obj_id: world[obj_id][RenderComponent].z_index
		)

	render_surface = pygame.Surface(cam_boundary["world_size"])
	for obj_id in sorted_entities:
		if SpacialComponent in world[obj_id]:
			obj = world[obj_id]
			obj_rect = obj[SpacialComponent].rect
			render_pos = obj_rect.left - camera_rect.left, obj_rect.top - camera_rect.top

			render_rect = pygame.Rect(render_pos, obj_rect.size)

			if obj[RenderComponent].sprite:
				render_surface.blit(obj[RenderComponent].sprite, render_rect)
			else:
				pygame.draw.rect(render_surface, obj[RenderComponent].color, render_rect)

	transformed_surface = pygame.transform.scale(render_surface, Settings.WINDOW.SIZE)
	surface.blit(transformed_surface, (0, 0))