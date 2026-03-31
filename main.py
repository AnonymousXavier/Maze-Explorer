import pygame

from Core.Game import Game
from ECS.Systems import AudioSystem, RenderingSystem, Input, GameStateManager
from Globals import Settings, Cache
from Core import States
from Misc.Mods_Manager import ModsManager

window = pygame.display.set_mode(Settings.WINDOW.SIZE, pygame.RESIZABLE)
pygame.display.set_caption(Settings.WINDOW.TITLE)

class Main:
    def __init__(self) -> None:
        self.game = Game()

        ModsManager.load_mods()
        ModsManager.trigger_engine_init(Settings, Cache)
        
        GameStateManager.init()

    def update(self):
        events = []
        dt = Settings.WINDOW.CLOCK.tick(Settings.WINDOW.FPS) / 1000

        Input.process(States.world, events)
        AudioSystem.process()
        GameStateManager.process(self.game, events, dt)

    def draw(self):
        window.fill(Settings.COLOURS.BLACK)
        RenderingSystem.process(window, States.world, States.spatial_grid, States.UI, States.camera)
        pygame.display.update()

    def run(self):
        while States.GAME_RUNNING:
            self.update()
            self.draw()

            if GameStateManager.game_ended_before:
                GameStateManager.reset()

Main().run()