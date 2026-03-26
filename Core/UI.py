import pygame

from Core import States
from ECS import Factories
from ECS.Components import SpacialComponent
from Globals import Settings


class UI:
	def __init__(self) -> None:
		self.main_menu_bg__id = Factories.new_panel(States.UI, Settings.WINDOW.DEFAULT_CENTER, Settings.WINDOW.DEFAULT_SIZE)
		self.easybutton_id: int = Factories.new_button(States.UI, "Easy (6x6)", (0, 0), (0, 0))
		self.mediumbutton_id: int = Factories.new_button(States.UI, "Medium (6x6)", (0, 0), (0, 0))
		self.hardbutton_id: int = Factories.new_button(States.UI, "Easy (6x6)", (0, 0), (0, 0))

		self.resize_and_position_elements()

	def resize_and_position_elements(self):
		ww, _ = Settings.WINDOW.DEFAULT_SIZE
		_, cy = Settings.WINDOW.DEFAULT_CENTER

		main_menu_rect: pygame.Rect = States.UI[self.main_menu_bg__id][SpacialComponent].rect

		easy_button_rect: pygame.Rect = States.UI[self.easybutton_id][SpacialComponent].rect
		
		easy_button_rect.centerx = main_menu_rect.centerx
		easy_button_rect.centery = cy * (1 + Settings.UI.BUTTON_DISTANCE_FROM_WINDOW_CENTER_AS_PERCENTAGE)


	def draw(self, surface: pygame.Surface):
		pass

	def update(self, events: list):
		pass