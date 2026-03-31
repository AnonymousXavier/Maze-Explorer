import pygame
from Globals import Settings
from ECS.Components import BackgroundComponent, ClickableComponent, SpacialComponent

frame = 0

def process(ui: dict):
	global frame
	if frame % (Settings.WINDOW.FPS / round(Settings.UPDATE.INPUTS_CHECKS_PER_SEC * 0.75)) == 0:
		mouse_pos = pygame.mouse.get_pos()
		for obj_id in ui:
			obj = ui[obj_id]
			if BackgroundComponent in obj and ClickableComponent in obj:
				rect: pygame.Rect = obj[SpacialComponent].rect
				is_hovered = rect.collidepoint(mouse_pos)
				clicked = pygame.mouse.get_pressed()[0]
				if is_hovered and clicked:
					obj[ClickableComponent].action()

	frame += 1
