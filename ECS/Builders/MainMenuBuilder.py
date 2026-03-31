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
	pw, ph = Settings.WINDOW.PREFERRED_SIZE
	cx, cy = Settings.WINDOW.DEFAULT_CENTER

	# The UI Works Perfectly with 1000.. so to make it respensive, everything is drawn relative to it
	tw, th = (pw // 4 , ph// 4)

	controls_sprite = pygame.transform.scale_by(Cache.SPRITES.MAIN_MENU.CONTROLS_SPRITES, 3)
	cover_art_sprite = pygame.transform.scale(Cache.SPRITES.MAIN_MENU.COVER_ART, (tw, th))

	lw, lh = pw - tw, ph // 2 - th

	bg_id = Factories.new_panel(ui, tag=MainMenuElementTag, center=(pw // 2, ph // 2), size=(pw, ph))
	maze_label_id = Factories.new_label(ui, text="         Maze", tag=MainMenuElementTag, center=(cx - lw // 2, 0), size=(lw, lh), bg_color=Settings.UI.PANEL_COLOR, text_color=Settings.COLOURS.CYAN)
	explorer_label_id = Factories.new_label(ui, text="     Explorer", tag=MainMenuElementTag, center=(cx - lw // 2, cy // 2 - lh // 2 + lh), size=(lw, lh), bg_color=Settings.UI.PANEL_COLOR, text_color=Settings.COLOURS.CYAN)

	maze_label_rect: pygame.Rect = ui[maze_label_id][SpacialComponent].rect
	maze_label_rect.midright = (pw - lw // 2.5, lh // 4)

	label_rect: pygame.Rect = ui[explorer_label_id][SpacialComponent].rect
	label_rect.midright = (pw - lw // 4.25, lh / 1.5)

	sw, sh = controls_sprite.get_size()
	Factories.new_image(ui, tag=MainMenuElementTag, center=(pw - sw // 2, ph - sh//2), sprite=controls_sprite)
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
	pw, ph = Settings.WINDOW.PREFERRED_SIZE

	# Find Optimal Button Seperation
	remaining_distance = (ph) * (1 -  Settings.UI.BUTTON_DISTANCE_FROM_WINDOW_CENTER_AS_PERCENTAGE)
	seperation = remaining_distance / (len(buttons) + 1)
	offset = seperation / 2

	y = (ph * Settings.UI.BUTTON_DISTANCE_FROM_WINDOW_CENTER_AS_PERCENTAGE) + seperation + offset
	for btn_id in buttons:
		btn_rect = States.UI[btn_id][SpacialComponent].rect
		btn_rect.centerx = pw // 4
		btn_rect.centery = y

		y += seperation

def start_game_with_size(btn_index: int):
	global selected_btn_ref_id, start_game

	selected_btn_ref_id = btn_index
	start_game = True


