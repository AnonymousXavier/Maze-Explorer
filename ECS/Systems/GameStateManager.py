from Core import States
from Core.Game import Game
from ECS.Builders import GameOverMenuBuilder, MainMenuBuilder, SuccessScreenBuilder
from Globals.Enums import STATES
from Globals import Settings
from ECS import Factories
from ECS.Systems import MenusUpdater
from ECS.Components import GameUIElementTag, SpacialComponent, TextComponent

fps_label_id = None
game_ended_before = False

def init():
    create_temp_camera()

def create_temp_camera():
    main_menu_bg_id = MainMenuBuilder.build(States.UI)
    States.camera = Factories.new_camera((0, 0), Settings.CAMERA.SIZE, main_menu_bg_id)

def reset(game: Game):
    global game_ended_before

    game_ended_before = False

    MainMenuBuilder.reset()
    GameOverMenuBuilder.reset()
    SuccessScreenBuilder.reset()

    game.reset()


    States.reset()
    create_temp_camera()

def add_fps_label_to_world():
	global fps_label_id

	fps_label_id = Factories.new_label(States.UI, text="60", tag = GameUIElementTag,text_color=Settings.COLOURS.CYAN)
    

def keep_fps_position_constant():
    px, py = Settings.WINDOW.PREFERRED_SIZE
    mx, my = Settings.UI.MARGIN * px, Settings.UI.MARGIN * py

    States.UI[fps_label_id][SpacialComponent].rect.bottomleft = mx, py - my

def manage_state_transitions(game: Game):
    global play_again, game_ended_before

    if States.CURRENT_GAME_STATE == STATES.SUCCESS or States.CURRENT_GAME_STATE == STATES.GAME_OVER:
        if GameOverMenuBuilder.change_to_main_menu or SuccessScreenBuilder.change_to_main_menu:
            States.CURRENT_GAME_STATE = STATES.MAIN_MENU
            game_ended_before = True

    if States.CURRENT_GAME_STATE == STATES.MAIN_MENU:
        if MainMenuBuilder.start_game:
            States.CURRENT_GAME_STATE = STATES.GAME
            if game_ended_before:
                play_again = True
            else:
                update_game_settings_with_selected_option()
                game.init()
                add_fps_label_to_world()
                MainMenuBuilder.start_game = False

    elif States.CURRENT_GAME_STATE == STATES.GAME:
        if game.return_to_main_menu:
            if game.player_caught:
                States.CURRENT_GAME_STATE = STATES.GAME_OVER
                GameOverMenuBuilder.build(States.UI)
            else:
                States.CURRENT_GAME_STATE = STATES.SUCCESS
                SuccessScreenBuilder.build(States.UI)

            game.return_to_main_menu = False

def process(game: Game, events: list, dt: float):
    manage_state_transitions(game)

    if States.CURRENT_GAME_STATE != STATES.GAME:
        MenusUpdater.process(States.UI)
    else:
        game.update(events, dt)
        States.UI[fps_label_id][TextComponent].text = str(round(Settings.WINDOW.CLOCK.get_fps()))
        keep_fps_position_constant()

def update_game_settings_with_selected_option():
    i = MainMenuBuilder.selected_btn_ref_id
    size = Settings.MAIN_MENU_GAME_MODES.VALUES[i]

    Settings.MAP.ROWS = size
    Settings.MAP.COLS = size

    Settings.update_map_constants()