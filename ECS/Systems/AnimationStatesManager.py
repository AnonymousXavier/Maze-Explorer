from ECS.Components import AnimationComponent
from Globals import Enums

tuples_directions_dict = {
	(0, 1): Enums.DIRECTIONS.DOWN,
	(1, 0): Enums.DIRECTIONS.RIGHT,
	(0, -1): Enums.DIRECTIONS.UP,
	(-1, 0): Enums.DIRECTIONS.LEFT,
}

def process(world: dict, events: list):
	entities_wanting_to_move = {}

	for event in events:
		if event["type"] == Enums.EventType.MOVEMENT_INTENT:
			entities_wanting_to_move[event["entity_id"]] = event["dx"], event["dy"]

	for obj_id in world:
		update_animation(world, obj_id, entities_wanting_to_move)

def update_animation(world: dict, obj_id: int, entities_wanting_to_move: dict):
	obj = world[obj_id]

	if AnimationComponent in obj: # Is an animatable Object
		anim_obj = obj[AnimationComponent]
		if obj_id in entities_wanting_to_move:
			dx, dy = entities_wanting_to_move[obj_id]

			anim_obj.state = Enums.ANIM_STATES.WALK
			anim_obj.direction = tuples_directions_dict[(dx, dy)]
		else:
			anim_obj.state = Enums.ANIM_STATES.IDLE
		