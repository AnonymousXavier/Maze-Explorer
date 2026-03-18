import pygame

from ECS.Builders import LevelBuilder
from Globals import Settings
from Core import States
from ECS.Systems import CameraSystem, Input, Render, Movement
from ECS import Factories


class Main:
    def __init__(self) -> None:
        self.window = pygame.display.set_mode(Settings.WINDOW.SIZE)
        self.clock = pygame.Clock()

        player_id = Factories.spawn_player(States.world, States.spatial_grid, 0, 0)
        States.camera = Factories.new_camera((0, 0), Settings.CAMERA.SIZE, player_id)

        LevelBuilder.build_level(States.world, States.spatial_grid)

    def update(self):
        States.events = []

        Input.process(States.world, States.events)
        Movement.process(States.world, States.spatial_grid, States.events)
        CameraSystem.process(States.world, States.camera)

        self.clock.tick(Settings.WINDOW.FPS)

    def draw(self):
        self.window.fill(Settings.COLOURS.BLACK)
        
        Render.process(self.window, States.world, States.spatial_grid, States.camera)
        pygame.display.update()

    def run(self):
        while States.GAME_RUNNING:
            self.update()
            self.draw()


Main().run()