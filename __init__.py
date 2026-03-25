import pygame

from ECS.Builders import LevelBuilder
from Globals import Settings
from Core import States
from ECS.Systems import AINavigationSystem, AnimationSystem, CameraSystem, Input, InteractionSystem, RaycastSystem, Render, Movement, AnimationStatesManager, FloorManager, AIStatesManager
from ECS import Factories

class Main:
    def __init__(self) -> None:
        self.window = pygame.display.set_mode(Settings.WINDOW.SIZE, pygame.RESIZABLE)
        self.clock = pygame.Clock()
        self.has_spawned_guards = False 

        (px, py),(ax, ay) = LevelBuilder.build_level(States.world, States.spatial_grid)

        player_id = Factories.spawn_player(States.world, States.spatial_grid, px, py)
        States.camera = Factories.new_camera((0, 0), Settings.CAMERA.SIZE, player_id)
        Factories.spawn_artifact(States.world, States.spatial_grid, ax, ay)

        FloorManager.spawn_floor(States.world, States.spatial_grid, States.camera, 0, 0)

    def update(self):
        events = []
        dt = self.clock.tick(Settings.WINDOW.FPS) / 1000

        # Process Events First
        Input.process(States.world, events)
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

        # print(self.clock.get_fps())
        if not self.has_spawned_guards and States.GAME_STATES["picked_artifact"]:
            self.change_state_to_looking_for_player()
            self.has_spawned_guards = True

    def change_state_to_looking_for_player(self):
        LevelBuilder.spawn_guards(States.world, States.spatial_grid)

    def draw(self):
        self.window.fill(Settings.COLOURS.BLACK)
        
        Render.process(self.window, States.world, States.spatial_grid, States.camera)
        pygame.display.update()

    def run(self):
        while States.GAME_RUNNING:
            self.update()
            self.draw()


Main().run()