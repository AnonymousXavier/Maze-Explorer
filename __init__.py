import pygame

from ECS.Builders import LevelBuilder
from ECS.Components import AnimationComponent
from Globals import Settings, Enums
from Core import States
from ECS.Systems import AnimationSystem, CameraSystem, Input, RaycastSystem, Render, Movement, StatesManager, FloorManager
from ECS import Factories

player_id = -1 

class Main:
    def __init__(self) -> None:
        global player_id
        self.window = pygame.display.set_mode(Settings.WINDOW.SIZE)
        self.clock = pygame.Clock()

        (px, py),(ax, ay) = LevelBuilder.build_level(States.world, States.spatial_grid)

        player_id = Factories.spawn_player(States.world, States.spatial_grid, px, py)
        States.camera = Factories.new_camera((0, 0), Settings.CAMERA.SIZE, player_id)
        Factories.spawn_artifact(States.world, States.spatial_grid, ax, ay)

        FloorManager.spawn_floor(States.world, States.spatial_grid, States.camera, 0, 0)

    def update(self):

        directions = {
        Enums.DIRECTIONS.UP: -90,
        Enums.DIRECTIONS.RIGHT: 0,
        Enums.DIRECTIONS.DOWN: 90,
        Enums.DIRECTIONS.LEFT: 180,
        }

        events = [{"type": Enums.EventType.SEARCH_INTENT, "entity_id": player_id, "direction": directions[States.world[player_id][AnimationComponent].direction]}]
        dt = self.clock.tick(Settings.WINDOW.FPS) / 1000

        Input.process(States.world, events)
        Movement.process(States.world, States.spatial_grid, events, dt)
        AnimationSystem.process(States.world, dt)
        StatesManager.process(States.world, events)
        CameraSystem.process(States.world, States.camera, dt)
        FloorManager.process(States.world, States.spatial_grid, States.camera)
        RaycastSystem.process(States.world,States.spatial_grid, events)

        # print(self.clock.get_fps())

    def draw(self):
        self.window.fill(Settings.COLOURS.BLACK)
        
        Render.process(self.window, States.world, States.spatial_grid, States.camera)
        pygame.display.update()

    def run(self):
        while States.GAME_RUNNING:
            self.update()
            self.draw()


Main().run()