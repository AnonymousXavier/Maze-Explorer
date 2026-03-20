import pygame

from Core import States
from ECS.Components import ObstacleTag, SpacialComponent, RenderComponent, PlayerInputTag, StalkerComponent, StateComponent
from Globals import Cache, Enums, Settings, Misc

def new_camera(cams_topleft: tuple, cams_size: tuple, target_id: int):
	return {
		SpacialComponent: SpacialComponent(
			rect=pygame.Rect(cams_topleft, cams_size)),
		StalkerComponent: StalkerComponent(target_id=target_id)
	}

def spawn_player(world: dict, spatial_grid: dict, animations: dict, grid_x: int, grid_y: int):
	x, y = grid_x * Settings.SPRITES.WIDTH, grid_y * Settings.SPRITES.HEIGHT

	new_id = States.NEXT_ENTITY_ID
	States.NEXT_ENTITY_ID += 1

	player = {
		SpacialComponent: SpacialComponent(
			grid_pos= (grid_x, grid_y),
			rect=pygame.Rect(x, y, Settings.SPRITES.WIDTH, Settings.SPRITES.HEIGHT)
		),
		RenderComponent: RenderComponent(color=Settings.DEBUG.PLAYER_COLOR),
		PlayerInputTag: PlayerInputTag(),
		StateComponent: StateComponent(state=Enums.ANIM_STATES.IDLE)
	}

	world[new_id] = player
	animations[new_id] = {"frames": Cache.SPRITES.PLAYER.RED_NINJA, "current_frame": 0, "state": 0, "direction": Enums.DIRECTIONS.UP}
	Misc.register_entity_in_grid(new_id, (grid_x, grid_y), spatial_grid)

	return new_id

def spawn_wall(world: dict, spatial_grid: dict, grid_x: int, grid_y: int, sprite):
	x, y = grid_x * Settings.SPRITES.WIDTH, grid_y * Settings.SPRITES.HEIGHT

	new_id = States.NEXT_ENTITY_ID
	States.NEXT_ENTITY_ID += 1

	wall = {
		SpacialComponent: SpacialComponent(
			grid_pos= (grid_x, grid_y),
			rect=pygame.Rect(x, y, Settings.SPRITES.WIDTH, Settings.SPRITES.HEIGHT)
		),
		RenderComponent: RenderComponent(color=Settings.DEBUG.WALL_COLOR, sprite=sprite),
		ObstacleTag: ObstacleTag()
	}

	world[new_id] = wall
	Misc.register_entity_in_grid(new_id, (grid_x, grid_y), spatial_grid)

	return new_id

def spawn_door(world: dict, spatial_grid: dict, grid_x: int, grid_y: int, sprite):
	x, y = grid_x * Settings.SPRITES.WIDTH, grid_y * Settings.SPRITES.HEIGHT

	new_id = States.NEXT_ENTITY_ID
	States.NEXT_ENTITY_ID += 1

	door = {
		SpacialComponent: SpacialComponent(
			grid_pos= (grid_x, grid_y),
			rect=pygame.Rect(x, y, Settings.SPRITES.WIDTH, Settings.SPRITES.HEIGHT)
		),
		RenderComponent: RenderComponent(color=Settings.DEBUG.DOOR_COLOR, sprite=sprite)
	}

	world[new_id] = door
	Misc.register_entity_in_grid(new_id, (grid_x, grid_y), spatial_grid)

	return new_id