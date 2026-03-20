from ECS.Components import RenderComponent, StateComponent

secs_passed_for_each_entity = {}

def process(world: dict, animations: dict, delta: float):
	for obj_id in animations:
		obj = world[obj_id]
		animation_obj = animations[obj_id]

		if RenderComponent in obj and StateComponent in obj:
			frames = animation_obj["frames"]
			state = animation_obj["state"]
			current_frame = animation_obj["current_frame"]
			direction = animation_obj["direction"]

			sprite = frames[state][direction]

			# only try to animate animations
			if type(sprite) == list:
				number_of_sprites = len(sprite)

				if obj_id not in secs_passed_for_each_entity:
					secs_passed_for_each_entity[obj_id] = 0

				animation_obj["current_frame"] = animate(obj_id, sprite, current_frame, number_of_sprites * 1.5)
				sprite = sprite[animation_obj["current_frame"]]

			obj[RenderComponent].sprite = sprite

	for obj_id in secs_passed_for_each_entity:
		secs_passed_for_each_entity[obj_id] += delta

def animate(obj_id: int, frames: list, current_frame, fps: float):
	secs_passed = secs_passed_for_each_entity[obj_id]

	if secs_passed > (1 / fps):
		current_frame += 1
		secs_passed_for_each_entity[obj_id] = 0

	if current_frame >= len(frames):
		current_frame = 0

	return current_frame
