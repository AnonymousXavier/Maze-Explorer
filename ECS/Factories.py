import pygame

from Core import States
from ECS.Components import ObstacleTag, SpacialComponent, RenderComponent, PlayerInputTag, StalkerComponent
from Globals import Settings, Misc

def new_camera(cams_topleft: tuple, cams_size: tuple, target_id: int):
	return {
		SpacialComponent: SpacialComponent(
			rect=pygame.Rect(cams_topleft, cams_size)),
		StalkerComponent: StalkerComponent(target_id=target_id)
	}

def spawn_player(world: dict, spatial_grid: dict, grid_x: int, grid_y: int):
	x, y = grid_x * Settings.SPRITES.WIDTH, grid_y * Settings.SPRITES.HEIGHT

	new_id = States.NEXT_ENTITY_ID
	States.NEXT_ENTITY_ID += 1

	player = {
		SpacialComponent: SpacialComponent(
			grid_pos= (grid_x, grid_y),
			rect=pygame.Rect(x, y, Settings.SPRITES.WIDTH, Settings.SPRITES.HEIGHT)
		),
		RenderComponent: RenderComponent(color=Settings.DEBUG.PLAYER_COLOR),
		PlayerInputTag: PlayerInputTag()
	}

	world[new_id] = player
	Misc.register_entity_in_grid(new_id, (grid_x, grid_y), spatial_grid)

	return new_id

def spawn_wall(world: dict, spatial_grid: dict, grid_x: int, grid_y: int):
	x, y = grid_x * Settings.SPRITES.WIDTH, grid_y * Settings.SPRITES.HEIGHT

	new_id = States.NEXT_ENTITY_ID
	States.NEXT_ENTITY_ID += 1

	wall = {
		SpacialComponent: SpacialComponent(
			grid_pos= (grid_x, grid_y),
			rect=pygame.Rect(x, y, Settings.SPRITES.WIDTH, Settings.SPRITES.HEIGHT)
		),
		RenderComponent: RenderComponent(color=Settings.DEBUG.WALL_COLOR),
		ObstacleTag: ObstacleTag()
	}

	world[new_id] = wall
	Misc.register_entity_in_grid(new_id, (grid_x, grid_y), spatial_grid)

	return new_id

def spawn_door(world: dict, spatial_grid: dict, grid_x: int, grid_y: int):
	x, y = grid_x * Settings.SPRITES.WIDTH, grid_y * Settings.SPRITES.HEIGHT

	new_id = States.NEXT_ENTITY_ID
	States.NEXT_ENTITY_ID += 1

	door = {
		SpacialComponent: SpacialComponent(
			grid_pos= (grid_x, grid_y),
			rect=pygame.Rect(x, y, Settings.SPRITES.WIDTH, Settings.SPRITES.HEIGHT)
		),
		RenderComponent: RenderComponent(color=Settings.DEBUG.DOOR_COLOR)
	}

	world[new_id] = door
	Misc.register_entity_in_grid(new_id, (grid_x, grid_y), spatial_grid)

	return new_id