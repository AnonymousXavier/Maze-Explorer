import pygame

from Core.Game import Game
from Core.UI import UI
from ECS import Factories
from ECS.Components import SpacialComponent
from ECS.Systems import RenderingSystem, Input
from Globals import Settings
from Core import States

class Main:
    def __init__(self) -> None:
        self.window = pygame.display.set_mode(Settings.WINDOW.SIZE, pygame.RESIZABLE)
        self.clock = pygame.Clock()

        self.fps_label_id: int


        self.add_fps_label_to_world()
        self.ui = UI()
        States.camera = Factories.new_camera((0, 0), Settings.CAMERA.SIZE, self.ui.main_menu_bg__id)
        # self.game = Game()

    def add_fps_label_to_world(self):
        mx, my = Settings.UI.MARGIN * Settings.WINDOW.WIDTH, Settings.UI.MARGIN * Settings.WINDOW.HEIGHT
        self.fps_label_id = Factories.new_label(States.UI, "60")

        States.world[self.fps_label_id][SpacialComponent].rect.bottomleft = mx, Settings.WINDOW.HEIGHT - my

    def update(self):
        events = []
        dt = self.clock.tick(Settings.WINDOW.FPS) / 1000
        Input.process(States.world, events)

        # print(self.clock.get_fps())
        self.game.update(events, dt)

    def draw(self):
        self.window.fill(Settings.COLOURS.BLACK)

        RenderingSystem.process(self.window, States.world, States.spatial_grid, States.UI, States.camera)

        pygame.display.update()

    def run(self):
        while States.GAME_RUNNING:
            self.update()
            self.draw()


Main().run()