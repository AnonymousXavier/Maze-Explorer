import random
import pygame

from ECS.Components import AnimationComponent, GuardTag, PlayerInputTag, RayCastRegion
from Globals import Enums, Settings

tuples_directions_dict = {
	(0, 1): Enums.DIRECTIONS.DOWN,
	(1, 0): Enums.DIRECTIONS.RIGHT,
	(0, -1): Enums.DIRECTIONS.UP,
	(-1, 0): Enums.DIRECTIONS.LEFT,
}

angle_directions_dict = {
    Enums.DIRECTIONS.UP: -90,
    Enums.DIRECTIONS.RIGHT: 0,
    Enums.DIRECTIONS.DOWN: 90,
    Enums.DIRECTIONS.LEFT: 180,
}

secs_passed_for_each_guard = {} # For Rotations

def process(world: dict, events: list, delta: float):
	entities_wanting_to_move = {}

	for event in events:
		if event["type"] == Enums.EventType.MOVEMENT_INTENT:
			entities_wanting_to_move[event["entity_id"]] = event["dx"], event["dy"]

	for obj_id in world:
		update_animation(world, obj_id, entities_wanting_to_move)
		update_guard(world, events, obj_id)

	for obj_id in secs_passed_for_each_guard:
		secs_passed_for_each_guard[obj_id] += delta

def update_animation(world: dict, obj_id: int, entities_wanting_to_move: dict):
	obj = world[obj_id]

	if AnimationComponent in obj: # Isnt an animatable Object
		anim_obj = obj[AnimationComponent]
		if obj_id in entities_wanting_to_move:
			dx, dy = entities_wanting_to_move[obj_id]

			anim_obj.state = Enums.ANIM_STATES.WALK
			anim_obj.direction = tuples_directions_dict[(dx, dy)]
		else:
			anim_obj.state = Enums.ANIM_STATES.IDLE

def update_guard(world: dict, events: list, obj_id: int):
	secs_passed = 0
	if GuardTag in world[obj_id]:
		if obj_id not in secs_passed_for_each_guard:
			secs_passed_for_each_guard[obj_id] = 0
		else:
			secs_passed = secs_passed_for_each_guard[obj_id]

		if RayCastRegion in world[obj_id]:
			# PathFind to the first found entity
			for entity_id in world[obj_id][RayCastRegion].found_entities:
				pathfind_event = {"type": Enums.EventType.PATHFIND_INTENT, "entity_id": obj_id, "target_id": entity_id}
				events.append(pathfind_event)

		# Change Facing Direction
		if int(secs_passed) >= Settings.GAME.GUARD_CHANGE_DIRECTION_TIME_DELAY:
			direction_id = random.choice(Enums.DIRECTIONS.ALL)
			world[obj_id][AnimationComponent].direction = direction_id
			secs_passed_for_each_guard[obj_id] = 0

		if round(secs_passed) == int(secs_passed): 
			event = {"type": Enums.EventType.SEARCH_INTENT, "entity_id": obj_id, "direction": angle_directions_dict[world[obj_id][AnimationComponent].direction]}
			events.append(event)
		