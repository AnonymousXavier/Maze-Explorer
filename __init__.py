import pygame

from ECS.Builders import LevelBuilder
from Globals import Settings
from Core import States
from ECS.Systems import AnimationSystem, CameraSystem, Input, Render, Movement, StatesManager
from ECS import Factories


class Main:
    def __init__(self) -> None:
        self.window = pygame.display.set_mode(Settings.WINDOW.SIZE)
        self.clock = pygame.Clock()

        (px, py), _ = LevelBuilder.build_level(States.world, States.spatial_grid)

        player_id = Factories.spawn_player(States.world, States.spatial_grid, States.animations, px, py)
        States.camera = Factories.new_camera((0, 0), Settings.CAMERA.SIZE, player_id)

    def update(self):
        events = []
        dt = self.clock.tick(Settings.WINDOW.FPS) / 1000

        Input.process(States.world, events)
        Movement.process(States.world, States.spatial_grid, events, dt)
        AnimationSystem.process(States.world, States.animations, dt)
        StatesManager.process(States.world, States.animations, events)
        CameraSystem.process(States.world, States.camera, dt)

        print(self.clock.get_fps())

    def draw(self):
        self.window.fill(Settings.COLOURS.BLACK)
        
        Render.process(self.window, States.world, States.spatial_grid, States.camera)
        pygame.display.update()

    def run(self):
        while States.GAME_RUNNING:
            self.update()
            self.draw()


Main().run()