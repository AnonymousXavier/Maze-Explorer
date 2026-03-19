from ECS.Components import SpacialComponent, RenderComponent
from ECS.Systems import CameraSystem

import pygame

from Globals import Settings

def process(surface: pygame.Surface, world: dict, spatial_grid: dict, camera:dict):
	camera_rect: pygame.Rect = camera[SpacialComponent].rect

	cam_boundary = CameraSystem.get_boundary_of(camera)
	cam_left, cam_top = cam_boundary["left"], cam_boundary["top"]
	cam_right, cam_bottom = cam_boundary["right"], cam_boundary["bottom"]

	visible_renderable_entities = []
	for iy in range(cam_top, cam_bottom + 1):
		for ix in range(cam_left, cam_right + 1):
			if (ix, iy) in spatial_grid:
				for obj_id in spatial_grid[(ix, iy)]:
					if RenderComponent in world[obj_id]:
						visible_renderable_entities.append(obj_id)

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
			pygame.draw.rect(render_surface, obj[RenderComponent].color, render_rect)

	transformed_surface = pygame.transform.scale(render_surface, Settings.WINDOW.SIZE)
	surface.blit(transformed_surface, (0, 0))