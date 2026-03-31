import random

import pygame
from Core import States
from ECS.Systems import AINavigationSystem, InteractionSystem, RaycastSystem
from Globals import Cache
from Globals.Enums import STATES

pygame.mixer.pre_init(44100, -16, 2, 2048)

last_global_state = None
last_game_state = None

def play_bg_music(paths: list[str]):
	global song_path_playing_rn_path

	path = random.choice(paths)
	if last_global_state != States.CURRENT_GAME_STATE or last_game_state != States.TAKEN_ARTIFACT: 
		pygame.mixer.music.load(path)
		pygame.mixer.music.play()
		pygame.mixer.music.set_volume(0.5)
		song_path_playing_rn_path = path

def process():
	global last_game_state, last_global_state
	# BACKGROUND MUSIC
	match States.CURRENT_GAME_STATE:
		case STATES.MAIN_MENU:
			play_bg_music(Cache.AUDIO.BG_MUSIC_PATHS.MAIN_MENU)
		case STATES.GAME:
			if States.TAKEN_ARTIFACT:
				play_bg_music(Cache.AUDIO.BG_MUSIC_PATHS.SUSPENSE)
			else:
				play_bg_music(Cache.AUDIO.BG_MUSIC_PATHS.PEACEFUL)
		case STATES.SUCCESS:
			play_bg_music(Cache.AUDIO.BG_MUSIC_PATHS.SUCCESS)
		case STATES.GAME_OVER:
			play_bg_music(Cache.AUDIO.BG_MUSIC_PATHS.GAME_OVER)


	# SOUND EFFECTS
	if RaycastSystem.found_player:
		Cache.AUDIO.SOUND_EFFECTS.PLAYER_DETECTED.play()
		RaycastSystem.found_player = False
	if InteractionSystem.interaction_occured:
		Cache.AUDIO.SOUND_EFFECTS.ARTIFACT_COLLECTED.play()
		InteractionSystem.interaction_occured = False
	if AINavigationSystem.caught_player:
		Cache.AUDIO.SOUND_EFFECTS.GAME_OVER.play()
		AINavigationSystem.caught_player = False

	last_global_state = States.CURRENT_GAME_STATE
	last_game_state = States.TAKEN_ARTIFACT

