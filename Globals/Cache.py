import pygame
from ECS.Loaders.SpriteLoader import load_animation, load_sprite
from Globals import Enums, Settings

pygame.mixer.init()
pygame.init()

sprite_size = Settings.SPRITES.SIZE

tileset_dict = {
	"door_left_right":                   (1, 2),
	"door_top_bottom":                   (1, 1),
	# TEES 
	"wall_tee_top_bottom_right":         (0, 0),
	"wall_tee_top_bottom_right_left":    (1, 0),
	"wall_tee_top_bottom_left":          (2, 0),
	"wall_tee_bottom_left_right":        (2, 1),
	"wall_tee_top_right_left":           (0, 1),
	# NORMAL WALLS
	"top_left_wall":                     (3, 0),
	"top_middle_wall":                   (4, 0),
	"top_right_wall":                    (5, 0),
	"middle_left_wall":                  (3, 1),
	"floor":                             (4, 1),
	"middle_right_wall":                 (5, 1),
	"bottom_left_wall":                  (3, 2),
	"bottom_middle_wall":                (4, 2),
	"bottom_right_wall":                 (5, 2),
}

class SPRITES:
	TILESET = load_animation("Assets\\Sprites\\tileset.png", sprite_size)
	ARTIFACT = load_animation("Assets\\Sprites\\Artifacts.png", sprite_size)[0]
	EXTRACTION_POINT_MARKER = load_sprite("Assets\\Sprites\\ExtractionPointMarker.png")

	class MAIN_MENU:
		CONTROLS_SPRITES = load_sprite("Assets\\Sprites\\Menu\\Controls.png")
		COVER_ART = load_sprite("Assets\\Sprites\\Menu\\NinjaAdventure CoverArt.png")

	class PLAYER:
		red_ninja_walk = load_animation("Assets\\Sprites\\Player\\Red Ninja\\Walk.png", sprite_size, vertical=True)
		red_ninja_dead = load_sprite("Assets\\Sprites\\Player\\Red Ninja\\Dead.png")
		red_ninja_idle = load_animation("Assets\\Sprites\\Player\\Red Ninja\\Idle.png", sprite_size)

		RED_NINJA = {
			Enums.ANIM_STATES.DEAD: {
				Enums.DIRECTIONS.LEFT: red_ninja_dead,
				Enums.DIRECTIONS.RIGHT: red_ninja_dead,
				Enums.DIRECTIONS.UP: red_ninja_dead,
				Enums.DIRECTIONS.DOWN: red_ninja_dead
			},
			Enums.ANIM_STATES.WALK: {
				Enums.DIRECTIONS.LEFT: red_ninja_walk[Enums.DIRECTIONS.LEFT],
				Enums.DIRECTIONS.RIGHT: red_ninja_walk[Enums.DIRECTIONS.RIGHT],
				Enums.DIRECTIONS.UP: red_ninja_walk[Enums.DIRECTIONS.UP],
				Enums.DIRECTIONS.DOWN: red_ninja_walk[Enums.DIRECTIONS.DOWN]
			},
			Enums.ANIM_STATES.IDLE: {
				Enums.DIRECTIONS.LEFT: red_ninja_idle[0][Enums.DIRECTIONS.LEFT],
				Enums.DIRECTIONS.RIGHT: red_ninja_idle[0][Enums.DIRECTIONS.RIGHT],
				Enums.DIRECTIONS.UP: red_ninja_idle[0][Enums.DIRECTIONS.UP],
				Enums.DIRECTIONS.DOWN: red_ninja_idle[0][Enums.DIRECTIONS.DOWN]
			}
		}

	class ENEMY:
		guard_walk = load_animation("Assets\\Sprites\\Guards\\Walk.png", sprite_size, vertical=True)
		guard_idle = load_animation("Assets\\Sprites\\Guards\\Idle.png", sprite_size)
		
		GUARD = {
				Enums.ANIM_STATES.WALK: {
					Enums.DIRECTIONS.LEFT: guard_walk[Enums.DIRECTIONS.LEFT],
					Enums.DIRECTIONS.RIGHT: guard_walk[Enums.DIRECTIONS.RIGHT],
					Enums.DIRECTIONS.UP: guard_walk[Enums.DIRECTIONS.UP],
					Enums.DIRECTIONS.DOWN: guard_walk[Enums.DIRECTIONS.DOWN]
				},
				Enums.ANIM_STATES.IDLE: {
					Enums.DIRECTIONS.LEFT: guard_idle[0][Enums.DIRECTIONS.LEFT],
					Enums.DIRECTIONS.RIGHT: guard_idle[0][Enums.DIRECTIONS.RIGHT],
					Enums.DIRECTIONS.UP: guard_idle[0][Enums.DIRECTIONS.UP],
					Enums.DIRECTIONS.DOWN: guard_idle[0][Enums.DIRECTIONS.DOWN]
				}
		}

class AUDIO:
	class BG_MUSIC_PATHS:
		# Singles will contain duplicates cos of random function
		PEACEFUL = ["Assets\\Audio\\Game\\Peaceful_BG_Music.ogg", "Assets\\Audio\\Game\\Peaceful_BG_Music2.ogg"]
		SUSPENSE = ["Assets\\Audio\\Game\\Suspense_BG_Music.ogg", "Assets\\Audio\\Game\\Suspense_BG_Music.ogg"]
		GAME_OVER = ["Assets\\Audio\\Menu\\GameOverMenu.ogg", "Assets\\Audio\\Menu\\GameOverMenu.ogg"]
		MAIN_MENU = ["Assets\\Audio\\Menu\\MainMenu.ogg", "Assets\\Audio\\Menu\\MainMenu2.ogg"]
		SUCCESS = ["Assets\\Audio\\Menu\\SuccessMenu.ogg", "Assets\\Audio\\Menu\\SuccessMenu.ogg"]

	class SOUND_EFFECTS:
		ARTIFACT_COLLECTED = pygame.mixer.Sound("Assets\\Audio\\Game\\ArtifactCollected.wav")
		PLAYER_DETECTED = pygame.mixer.Sound("Assets\\Audio\\Game\\PlayerDetected.wav")
		GAME_OVER = pygame.mixer.Sound("Assets\\Audio\\Game\\GameOver.wav")