import pygame

from Globals import Settings
from Core import States
from ECS.Systems import Input, Render, Movement
from ECS import Factories


class Main:
    def __init__(self) -> None:
        self.window = pygame.display.set_mode(Settings.WINDOW.SIZE)
        self.clock = pygame.Clock()

        Factories.spawn_player(States.world, 0, 0)

    def draw(self):
        self.window.fill(Settings.COLOURS.BLACK)
        Render.process(self.window, States.world)

        pygame.display.update()

    def update(self):
        States.events = []

        Input.process(States.world, States.events)
        Movement.process(States.world, States.events)

        self.clock.tick(Settings.WINDOW.FPS)

    def run(self):
        while States.GAME_RUNNING:
            self.update()
            self.draw()


Main().run()