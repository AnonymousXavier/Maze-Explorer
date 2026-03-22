from ECS.Components import PlayerInputTag, RayCastRegion, SpacialComponent, RenderComponent
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

	cbw, cbh = cam_boundary["world_size"]
	px, py = -1, -1

	render_surface = pygame.Surface((cbw, cbh))
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

			if PlayerInputTag in world[obj_id]:
				px, py = render_rect.center

			if RayCastRegion in world[obj_id]:
				for (xi, yi) in world[obj_id][RayCastRegion].points:
					x, y = xi * Settings.SPRITES.WIDTH, yi * Settings.SPRITES.HEIGHT 
					render_pos = x - camera_rect.left, y - camera_rect.top
					render_rect = pygame.Rect(render_pos, Settings.SPRITES.SIZE)
					pygame.draw.rect(render_surface, Settings.DEBUG.RAYCAST_COLOR, render_rect)

	# Draw Overlay
	foggy_view_surface = pygame.Surface((cbw, cbh), pygame.SRCALPHA)
	foggy_view_surface.fill(Settings.COLOURS.BLACK)

	pygame.draw.circle(foggy_view_surface, Settings.COLOURS.ZERO_ALPHA, (px, py), cbw * Settings.GAME.PLAYER_LIGHT_RADIUS_AS_PERCENT_OF_SCREEN_AREA * 0.5)
	render_surface.blit(foggy_view_surface)

	transformed_surface = pygame.transform.scale(render_surface, Settings.WINDOW.SIZE)
	surface.blit(transformed_surface, (0, 0))