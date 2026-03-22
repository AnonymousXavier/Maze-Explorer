import pygame

from ECS.Builders import LevelBuilder
from Globals import Settings
from Core import States
from ECS.Systems import AnimationSystem, CameraSystem, Input, Render, Movement, StatesManager, FloorManager
from ECS import Factories


class Main:
    def __init__(self) -> None:
        self.window = pygame.display.set_mode(Settings.WINDOW.SIZE)
        self.clock = pygame.Clock()

        (px, py), _ = LevelBuilder.build_level(States.world, States.spatial_grid)

        player_id = Factories.spawn_player(States.world, States.spatial_grid, px, py)
        States.camera = Factories.new_camera((0, 0), Settings.CAMERA.SIZE, player_id)

        FloorManager.spawn_floor(States.world, States.spatial_grid, States.camera, 0, 0)

    def update(self):
        events = []
        dt = self.clock.tick(Settings.WINDOW.FPS) / 1000

        Input.process(States.world, events)
        Movement.process(States.world, States.spatial_grid, events, dt)
        AnimationSystem.process(States.world, dt)
        StatesManager.process(States.world, events)
        CameraSystem.process(States.world, States.camera, dt)
        FloorManager.process(States.world, States.spatial_grid, States.camera)

    def draw(self):
        self.window.fill(Settings.COLOURS.BLACK)
        
        Render.process(self.window, States.world, States.spatial_grid, States.camera)
        pygame.display.update()

    def run(self):
        while States.GAME_RUNNING:
            self.update()
            self.draw()


Main().run()