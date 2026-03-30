import pygame
from ECS.Components import BackgroundComponent, HoverComponent, SpacialComponent

def process(ui: dict):
	mouse_pos = pygame.mouse.get_pos()
	for obj_id in ui:
		obj = ui[obj_id]
		if HoverComponent in obj and BackgroundComponent in obj:
			rect: pygame.Rect = obj[SpacialComponent].rect
			is_hovered = rect.collidepoint(mouse_pos)
			if is_hovered:
				obj[BackgroundComponent].color = obj[HoverComponent].hovered_color
			else:
				obj[BackgroundComponent].color = obj[HoverComponent].normal_color
