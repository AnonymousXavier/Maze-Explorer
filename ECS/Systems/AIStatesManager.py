import random
from ECS.Components import AnimationComponent, GuardTag, RayCastRegion, AIStateComponent
from Globals import Enums, Settings

secs_passed_for_each_guard = {} # For Rotations

angle_directions_dict = {
    Enums.DIRECTIONS.UP: -90,
    Enums.DIRECTIONS.RIGHT: 0,
    Enums.DIRECTIONS.DOWN: 90,
    Enums.DIRECTIONS.LEFT: 180,
}

def process(world: dict, events: list, delta: float):
	global secs_passed

	for obj_id in world:
		if GuardTag in world[obj_id]:
			secs_passed = 0

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
				world[obj_id][AIStateComponent].state = Enums.AI_STATES.PATHFIND
				event = {"type": Enums.EventType.SEARCH_INTENT, "entity_id": obj_id, "direction": angle_directions_dict[world[obj_id][AnimationComponent].direction]}
				events.append(event)

	for obj_id in secs_passed_for_each_guard:
		secs_passed_for_each_guard[obj_id] += delta