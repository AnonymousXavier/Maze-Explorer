from Globals.Enums import STATES


world = {}
spatial_grid = {} 
camera = {}
UI = {}

TAKEN_ARTIFACT = False
GAME_RUNNING = True

CURRENT_GAME_STATE = STATES.MAIN_MENU


NEXT_ENTITY_ID = 1
NEXT_UI_ELEMENT_ID = 1

def reset():
	global world, spatial_grid, camera, UI, TAKEN_ARTIFACT, GAME_RUNNING, CURRENT_GAME_STATE, NEXT_ENTITY_ID, NEXT_UI_ELEMENT_ID
	world = {}
	spatial_grid = {} 
	camera = {}
	UI = {}

	TAKEN_ARTIFACT = False
	GAME_RUNNING = True

	CURRENT_GAME_STATE = STATES.MAIN_MENU


	NEXT_ENTITY_ID = 1
	NEXT_UI_ELEMENT_ID = 1