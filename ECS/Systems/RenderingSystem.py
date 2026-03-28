from Core import States
from ECS.Components import BackgroundComponent, PlayerInputTag, RayCastRegion, SpacialComponent, RenderComponent, TextComponent
from ECS.Systems import CameraSystem

import pygame

from Globals import  Misc, Settings

def process(surface: pygame.Surface, world: dict, spatial_grid: dict, UI: dict, camera:dict):
	camera_rect: pygame.Rect = camera[SpacialComponent].rect
	cam_boundary = CameraSystem.get_boundary_of(camera)
	cbw, cbh = cam_boundary["world_size"]
	
	game_entities_rendered_surface = draw_game_entities(world, spatial_grid, cam_boundary, camera_rect)
	ui_elements_rendered_surface = draw_ui(States.UI)

	# FOR WINDOW RESIZ-ING
	scale_x = Settings.WINDOW.WIDTH / cbw
	scale_y = Settings.WINDOW.HEIGHT / cbh
	scale = min(scale_x, scale_y) 
	
	new_w = int(cbw * scale)
	new_h = int(cbh * scale)
	
	entities_transformed_surface = pygame.transform.scale(game_entities_rendered_surface, (new_w, new_h))
	ui_transformed_surface = pygame.transform.scale(ui_elements_rendered_surface, (new_w, new_h))

	x_offset = (Settings.WINDOW.WIDTH - new_w) // 2
	y_offset = (Settings.WINDOW.HEIGHT - new_h) // 2
	
	surface.fill(Settings.COLOURS.BLACK)
	surface.blit(entities_transformed_surface, (x_offset, y_offset))
	surface.blit(ui_transformed_surface, (x_offset, y_offset))

def draw_game_entities(world: dict, spatial_grid: dict, cam_boundary: dict, camera_rect):
	px, py = -1, -1
	cbw, cbh = cam_boundary["world_size"]

	visible_renderable_entities = Misc.get_visible_entities_with(world, spatial_grid, cam_boundary, RenderComponent)

	sorted_entities = sorted(
		visible_renderable_entities,
		key=lambda obj_id: world[obj_id][RenderComponent].z_index
		)

	render_surface = pygame.Surface((cbw, cbh))
	for obj_id in sorted_entities:
		if SpacialComponent in world[obj_id]:
			obj = world[obj_id]
			obj_rect = obj[SpacialComponent].rect
			render_pos = obj_rect.left - camera_rect.left, obj_rect.top - camera_rect.top

			render_rect = pygame.Rect(render_pos, obj_rect.size)

			if RayCastRegion in world[obj_id]:
				cone_surface = world[obj_id][RayCastRegion].shape
				pix, piy = world[obj_id][RayCastRegion].pivot
				rx, ry = pix - camera_rect.left, piy - camera_rect.top
				render_surface.blit(cone_surface, (rx, ry))

			if obj[RenderComponent].sprite:
				render_surface.blit(obj[RenderComponent].sprite, render_rect)
			else:
				pygame.draw.rect(render_surface, obj[RenderComponent].color, render_rect)

			if PlayerInputTag in world[obj_id]:
				px, py = render_rect.center

	# Draw Overlay
	if States.TAKEN_ARTIFACT: # Now Looking for player
		foggy_view_surface = pygame.Surface((cbw, cbh), pygame.SRCALPHA)
		foggy_view_surface.fill(Settings.COLOURS.BLACK)

		pygame.draw.circle(foggy_view_surface, Settings.COLOURS.ZERO_ALPHA, (px, py), cbw * Settings.GAME.PLAYER_LIGHT_RADIUS_AS_PERCENT_OF_SCREEN_AREA * 0.5)
		render_surface.blit(foggy_view_surface)

	return render_surface

def draw_ui(UI: dict):
	render_surface = pygame.Surface(Settings.WINDOW.DEFAULT_SIZE, pygame.SRCALPHA)
	for element_id in UI:
		element = UI[element_id]
		if SpacialComponent in element:
			if BackgroundComponent in element:
				if TextComponent not in element:
					pygame.draw.rect(render_surface, element[BackgroundComponent].color, element[SpacialComponent].rect)
				else:
					text_surface = Settings.UI.FONT.render(UI[element_id][TextComponent].text, True, UI[element_id][TextComponent].color)
					tw, th = text_surface.size
					factor = (1 + Settings.UI.TEXT_PADDING_AS_PERCENTAGE_OF_SIZE)
					bg_size = tw * factor, th * factor

					render_rect = pygame.Rect((0, 0), bg_size)
					render_rect.center = element[SpacialComponent].rect.center

					print(element[SpacialComponent].rect)

					pygame.draw.rect(render_surface, element[BackgroundComponent].color, render_rect)
					render_surface.blit(text_surface, text_surface.get_rect(center=render_rect.center))

	return render_surface