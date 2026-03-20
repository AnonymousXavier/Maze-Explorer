from ECS.Loaders.SpriteLoader import load_animation
from Globals import Enums, Settings

sprite_size = Settings.SPRITES.SIZE

tileset_dict = {
	# DOOR BEAM
	"left_upper_door_beam":  (0, 0),
	"up_upper_door_beam":    (1, 0),
	"up_lower_door_beam":    (2, 0),
	"left_lower_door_beam":  (0, 1),
	"door":                  (1, 1),
	"right_upper_door_beam": (2, 1),
	"down_upper_door_beam":  (0, 2),
	"down_lower_door_beam":  (1, 2),
	"right_lower_door_beam": (2, 2),
	# WALLS
	"top_left_wall":         (3, 0),
	"top_middle_wall":       (4, 0),
	"top_right_wall":        (5, 0),
	"middle_left_wall":      (3, 1),
	"floor":                 (4, 1),
	"middle_right_wall":     (5, 1),
	"bottom_left_wall":      (3, 2),
	"bottom_middle_wall":    (4, 2),
	"bottom_right_wall":     (5, 2),
}

class SPRITES:
	TILESET = load_animation = load_animation("Assets\\Sprites\\tileset.png", sprite_size)
	class PLAYER:
		red_ninja_walk = load_animation("Assets\\Sprites\\Player\\Red Ninja\\Walk.png", sprite_size, vertical=True)
		red_ninja_attack = load_animation("Assets\\Sprites\\Player\\Red Ninja\\Attack.png", sprite_size)
		red_ninja_idle = load_animation("Assets\\Sprites\\Player\\Red Ninja\\Idle.png", sprite_size)

		RED_NINJA = {
			Enums.ANIM_STATES.ATTACK: {
				Enums.DIRECTIONS.LEFT: red_ninja_attack[0][Enums.DIRECTIONS.LEFT],
				Enums.DIRECTIONS.RIGHT: red_ninja_attack[0][Enums.DIRECTIONS.RIGHT],
				Enums.DIRECTIONS.UP: red_ninja_attack[0][Enums.DIRECTIONS.UP],
				Enums.DIRECTIONS.DOWN: red_ninja_attack[0][Enums.DIRECTIONS.DOWN]
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
