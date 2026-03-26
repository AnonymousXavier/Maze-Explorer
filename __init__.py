import pygame

from Core.Game import Game
from Core.UI import UI
from ECS import Factories
from ECS.Systems import RenderingSystem, Input
from Globals import Settings
from Core import States

class Main:
    def __init__(self) -> None:
        self.window = pygame.display.set_mode(Settings.WINDOW.SIZE, pygame.RESIZABLE)
        self.clock = pygame.Clock()

        self.ui = UI()
        States.camera = Factories.new_camera((0, 0), Settings.CAMERA.SIZE, self.ui.main_menu_bg__id)
        # self.game = Game()

    def update(self):
        events = []
        dt = self.clock.tick(Settings.WINDOW.FPS) / 1000
        Input.process(States.world, events)
        # self.game.update(events, dt)

    def draw(self):
        self.window.fill(Settings.COLOURS.BLACK)

        RenderingSystem.process(self.window, States.world, States.spatial_grid, States.UI, States.camera)

        pygame.display.update()

    def run(self):
        while States.GAME_RUNNING:
            self.update()
            self.draw()


Main().run()