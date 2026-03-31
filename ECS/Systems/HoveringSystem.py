import pygame
from Globals import Settings
from ECS.Components import BackgroundComponent, HoverComponent, SpacialComponent

def process(ui: dict):
	mouse_pos = pygame.mouse.get_pos()

	ww, wh = Settings.WINDOW.SIZE
	pw, ph = Settings.WINDOW.PREFERRED_SIZE

	for obj_id in ui:
		obj = ui[obj_id]
		if HoverComponent in obj and BackgroundComponent in obj:
			rect: pygame.Rect = obj[SpacialComponent].rect

			x, y = rect.topleft
			w, h = rect.size
			rx, ry = x * ww // pw, y * wh // ph 
			rw, rh = w * ww // pw, h * wh // ph
			render_rect = pygame.Rect((rx, ry), (rw, rh)) # Actual Position on screen

			is_hovered = render_rect.collidepoint(mouse_pos)
			if is_hovered:
				obj[BackgroundComponent].color = obj[HoverComponent].hovered_color
			else:
				obj[BackgroundComponent].color = obj[HoverComponent].normal_color
