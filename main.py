import pygame

from Scripts.Core.Map.world_generator import world_generator
from Scripts.Globals import Settings


class Main:
    def __init__(self) -> None:
        self.window = pygame.display.set_mode(Settings.WINDOW.SIZE)
        self.running = True
        self.world_gen = world_generator()


    def draw(self):
        self.world_gen.draw(self.window)

    def update(self):
        self.handle_events()

        pygame.display.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def run(self):
        while self.running:
            self.update()
            self.draw()


Main().run()