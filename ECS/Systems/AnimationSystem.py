from ECS.Components import AnimationComponent, RenderComponent, StateComponent

secs_passed_for_each_entity = {}

def process(world: dict, delta: float):
	for obj_id in world:
		obj = world[obj_id]

		if AnimationComponent in obj:
			if RenderComponent in obj and StateComponent in obj:
				frames = obj[AnimationComponent].frames
				state = obj[AnimationComponent].state
				current_frame = obj[AnimationComponent].current_frame
				direction = obj[AnimationComponent].direction

				sprite = frames[state][direction]

				# only try to animate animations
				if type(sprite) == list:
					number_of_sprites = len(sprite)

					if obj_id not in secs_passed_for_each_entity:
						secs_passed_for_each_entity[obj_id] = 0

					obj[AnimationComponent].current_frame = animate(obj_id, sprite, current_frame, number_of_sprites * 1.5)
					sprite = sprite[obj[AnimationComponent].current_frame]

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
