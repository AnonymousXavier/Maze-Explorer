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

        (px, py), _ = LevelBuilder.build_level(States.world, States.spatial_grid)

        player_id = Factories.spawn_player(States.world, States.spatial_grid, px, py)
        States.camera = Factories.new_camera((0, 0), Settings.CAMERA.SIZE, player_id)
        self.frame = 0

    def update(self):
        States.events = []
        dt = self.clock.tick(Settings.WINDOW.FPS) / 1000

        if self.frame % (Settings.WINDOW.FPS / Settings.WINDOW.INPUTS_CHECKS_PER_SEC) == 0:
            Input.process(States.world, States.events)
        
        Movement.process(States.world, States.spatial_grid, States.events, dt)
        CameraSystem.process(States.world, States.camera, dt)

        self.frame += 1


    def draw(self):
        self.window.fill(Settings.COLOURS.BLACK)
        
        Render.process(self.window, States.world, States.spatial_grid, States.camera)
        pygame.display.update()

    def run(self):
        while States.GAME_RUNNING:
            self.update()
            self.draw()


Main().run()