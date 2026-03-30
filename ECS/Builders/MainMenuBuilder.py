from functools import partial
import pygame

from Core import States
from ECS import Factories
from ECS.Components import MainMenuElementTag, SpacialComponent
from Globals import Cache, Settings

selected_btn_ref_id = 0
start_game = False

def reset():
	global selected_btn_ref_id, start_game
	selected_btn_ref_id = 0
	start_game = False

def build(ui: dict):
	cx, cy = Settings.WINDOW.DEFAULT_CENTER
	ww, wh = Settings.WINDOW.DEFAULT_SIZE

	tw, th = (ww // 4, wh // 4)

	controls_sprite = pygame.transform.scale_by(Cache.SPRITES.MAIN_MENU.CONTROLS_SPRITES, 3)
	cover_art_sprite = pygame.transform.scale(Cache.SPRITES.MAIN_MENU.COVER_ART, (tw, th))

	lw, lh = ww - tw, wh // 2 - th
	bg_id = Factories.new_panel(ui, tag=MainMenuElementTag, center=Settings.WINDOW.DEFAULT_CENTER, size=Settings.WINDOW.DEFAULT_SIZE)
	maze_label_id = Factories.new_label(ui, text="         Maze", tag=MainMenuElementTag, center=(cx - lw // 2, 0), size=(lw, lh), bg_color=Settings.UI.PANEL_COLOR, text_color=Settings.COLOURS.CYAN)
	explorer_label_id = Factories.new_label(ui, text="     Explorer", tag=MainMenuElementTag, center=(cx - lw // 2, cy // 2 - lh // 2 + lh), size=(lw, lh), bg_color=Settings.UI.PANEL_COLOR, text_color=Settings.COLOURS.CYAN)

	maze_label_rect: pygame.Rect = ui[maze_label_id][SpacialComponent].rect
	maze_label_rect.midright = (ww - lw // 2.5, lh // 4)

	label_rect: pygame.Rect = ui[explorer_label_id][SpacialComponent].rect
	label_rect.midright = (ww - lw // 4.25, lh / 1.5)

	sw, sh = controls_sprite.get_size()
	Factories.new_image(ui, tag=MainMenuElementTag, center=(ww - sw // 2, wh - sh//2), sprite=controls_sprite)
	Factories.new_image(ui, tag=MainMenuElementTag, center=(tw // 2, th // 2), sprite=cover_art_sprite)
	buttons = initialize_buttons()

	position_elements(buttons)

	return bg_id

def initialize_buttons():
	buttons = []
	for i, title in enumerate(Settings.MAIN_MENU_GAME_MODES.TITLES):
		action = partial(start_game_with_size, i)
		btn_id = Factories.new_button(States.UI, text=title, tag=MainMenuElementTag, action=action)
		buttons.append(btn_id)

	return buttons

def position_elements(buttons: list):
	ww, wh = Settings.WINDOW.DEFAULT_SIZE

	# Find Optimal Button Seperation
	remaining_distance = (wh) * (1 -  Settings.UI.BUTTON_DISTANCE_FROM_WINDOW_CENTER_AS_PERCENTAGE)
	seperation = remaining_distance / (len(buttons) + 1)
	offset = seperation / 2

	y = (wh * Settings.UI.BUTTON_DISTANCE_FROM_WINDOW_CENTER_AS_PERCENTAGE) + seperation + offset
	for btn_id in buttons:
		btn_rect = States.UI[btn_id][SpacialComponent].rect
		btn_rect.centerx = ww // 4
		btn_rect.centery = y

		y += seperation

def start_game_with_size(btn_index: int):
	global selected_btn_ref_id, start_game

	selected_btn_ref_id = btn_index
	start_game = True


