from ECS.Builders import LevelBuilder
from Globals import Settings
from Core import States
from ECS.Systems import AINavigationSystem, AnimationSystem, CameraSystem, InteractionSystem, RaycastSystem, Movement, AnimationStatesManager, FloorManager, AIStatesManager
from ECS import Factories

class Game:
	def __init__(self) -> None:
		self.has_spawned_guards = False 

		(px, py),(ax, ay) = LevelBuilder.build_level(States.world, States.spatial_grid)
        
		Factories.spawn_extraction_point(States.world, States.spatial_grid, px, py, self.change_game_state)
		player_id = Factories.spawn_player(States.world, States.spatial_grid, px, py)

		States.camera = Factories.new_camera((0, 0), Settings.CAMERA.SIZE, player_id)

		Factories.spawn_artifact(States.world, States.spatial_grid, ax, ay, self.transition_to_chase)
		FloorManager.spawn_floor(States.world, States.spatial_grid, States.camera, 0, 0)

	def update(self, events: list, dt: float):
		# Process Events First
		AIStatesManager.process(States.world, events, dt)
		RaycastSystem.process(States.world,States.spatial_grid, events)
		AINavigationSystem.process(States.world, States.spatial_grid, events)

		# Handle Games Core
		InteractionSystem.process(States.world, States.spatial_grid, events)
		AnimationStatesManager.process(States.world, events)
		Movement.process(States.world, States.spatial_grid, events, dt)
		AnimationSystem.process(States.world, dt)
		CameraSystem.process(States.world, States.camera, dt)
		FloorManager.process(States.world, States.spatial_grid, States.camera)

		if not self.has_spawned_guards and States.TAKEN_ARTIFACT:
			self.change_state_to_looking_for_player()
			self.has_spawned_guards = True

	def change_state_to_looking_for_player(self):
		LevelBuilder.spawn_guards(States.world, States.spatial_grid)

	def change_game_state(self):
		if States.TAKEN_ARTIFACT:
			print("Game Completed")
			return True
		
		print("Steal Artiface, we're waiting for you")

	def transition_to_chase(self):
		States.TAKEN_ARTIFACT = True

		return True
