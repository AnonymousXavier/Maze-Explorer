from Globals import Enums

directions = {
	(0, 1): Enums.DIRECTIONS.DOWN,
	(1, 0): Enums.DIRECTIONS.RIGHT,
	(0, -1): Enums.DIRECTIONS.UP,
	(-1, 0): Enums.DIRECTIONS.LEFT,
}

def process(world: dict, animations: dict, events: list):
	entities_wanting_to_move = {}
	
	for event in events:
		if event["type"] == Enums.EventType.MOVEMENT_INTENT:
			entities_wanting_to_move[event["entity_id"]] = event["dx"], event["dy"]

	for obj_id in world:
		if obj_id in animations: # Isnt an animatable Object
			anim_obj = animations[obj_id]
			if obj_id in entities_wanting_to_move:
				dx, dy = entities_wanting_to_move[obj_id]

				anim_obj["state"] = Enums.ANIM_STATES.WALK
				anim_obj["direction"] = directions[(dx, dy)]
			else:
				anim_obj["state"] = Enums.ANIM_STATES.IDLE
				anim_obj["direction"] = Enums.DIRECTIONS.DOWN
		