import pygame

from Core import States
from ECS import Factories
from ECS.Components import GameOverElementTag, SpacialComponent
from Globals import Settings

change_to_main_menu = False

def build(ui: dict):
    pw, ph = Settings.WINDOW.PREFERRED_SIZE
    cx, cy = pw // 2, ph // 2

    # Create elements
    bg_id = Factories.new_panel(ui, tag=GameOverElementTag, center=(cx, cy), size=(pw, ph))
    Factories.new_label(ui, text="You Got Caught", tag=GameOverElementTag, center=(cx, cy // 2), size=(cx, cy // 2), bg_color=Settings.UI.PANEL_COLOR, text_color=Settings.COLOURS.RED)
    return_btn_id = Factories.new_button(States.UI, text="Return to main menu", tag=GameOverElementTag, action=return_to_main_menu)

    # Derive Buttons Position using relative height (ph)
    remaining_distance = ph * (1 - Settings.UI.BUTTON_DISTANCE_FROM_WINDOW_CENTER_AS_PERCENTAGE)
    button_center_from_screen_center = remaining_distance / 2

    # Get Rects
    main_menu_rect: pygame.Rect = States.UI[bg_id][SpacialComponent].rect
    return_btn_rect = States.UI[return_btn_id][SpacialComponent].rect

    # Position It relative to the preferred center (cy)
    return_btn_rect.centerx = main_menu_rect.centerx
    return_btn_rect.centery = cy + button_center_from_screen_center

    return bg_id

def reset():
    global change_to_main_menu
    change_to_main_menu = False

def return_to_main_menu():
    global change_to_main_menu
    change_to_main_menu = True