from typing import Callable
import pygame
import random


from Core import States
from Globals import Cache, Enums, Settings, Misc
from ECS.Components import (AIStateComponent, AnimationComponent, ArtifactTag, 
	BackgroundComponent, ClickableComponent, ExtractionTag, GuardTag, InteractableComponent, 
	ObstacleTag, PathFindingComponent, RayCastComponent, SpacialComponent, RenderComponent, 
	PlayerInputTag, StalkerComponent, AnimationStateComponent, HoverComponent, TextComponent,
	InteractorComponent)


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
		PlayerInputTag: PlayerInputTag(),
		AnimationStateComponent: AnimationStateComponent(state=Enums.ANIM_STATES.IDLE),
		AnimationComponent: AnimationComponent(
			frames=Cache.SPRITES.PLAYER.RED_NINJA,
			current_frame=0,
			state=0,
			direction=Enums.DIRECTIONS.DOWN,
		),
		InteractorComponent: InteractorComponent(mask=(ArtifactTag, ExtractionTag))
	}

	world[new_id] = player
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

def generate_and_spawn_floor_sprite(world: dict, spatial_grid: dict, cam_boundary: dict, grid_x: int, grid_y: int, sprite):
	cam_left, cam_top = cam_boundary["left"], cam_boundary["top"]
	cam_right, cam_bottom = cam_boundary["right"], cam_boundary["bottom"]

	new_id = States.NEXT_ENTITY_ID
	States.NEXT_ENTITY_ID += 1

	top, bottom = cam_top - 1, cam_bottom + 2
	left, right = cam_left - 1, cam_right + 2

	w, h = right - left, bottom - top
	spr_size = w * Settings.SPRITES.WIDTH, h * Settings.SPRITES.HEIGHT

	floor_surface = pygame.Surface(spr_size)
	for iy in range(top, bottom):
		for ix in range(left, right):
			x = (ix - left) * Settings.SPRITES.WIDTH
			y = (iy - top) * Settings.SPRITES.HEIGHT

			floor_surface.blit(sprite, (x, y))

	floor = {
		SpacialComponent: SpacialComponent(
			grid_pos= (grid_x, grid_y),
			rect=pygame.Rect(
				(grid_x * Settings.SPRITES.WIDTH, grid_y * Settings.SPRITES.HEIGHT), 
				spr_size
			)
		),
		RenderComponent: RenderComponent(
			color=Settings.DEBUG.FLOOR_COLOR,
			sprite=floor_surface,
			z_index = -1
		)
	}

	world[new_id] = floor
	Misc.register_entity_in_grid(new_id, (grid_x, grid_y), spatial_grid)

	return new_id

def spawn_artifact(world: dict, spatial_grid: dict, grid_x: int, grid_y: int, action: Callable):
	x, y = grid_x * Settings.SPRITES.WIDTH, grid_y * Settings.SPRITES.HEIGHT

	new_id = States.NEXT_ENTITY_ID
	States.NEXT_ENTITY_ID += 1

	artifact = {
		SpacialComponent: SpacialComponent(
			grid_pos=(grid_x, grid_y),
			rect=pygame.Rect(x, y, Settings.SPRITES.WIDTH, Settings.SPRITES.HEIGHT)
			),
		RenderComponent: RenderComponent(
			color=Settings.DEBUG.ARTIFACT_COLOR,
			sprite=random.choice(Cache.SPRITES.ARTIFACT)
			),
		ArtifactTag: ArtifactTag(),
		InteractableComponent: InteractableComponent(layer=ArtifactTag, action=action)
	}

	world[new_id] = artifact
	Misc.register_entity_in_grid(new_id, (grid_x, grid_y), spatial_grid)

	return new_id

def spawn_raycasted_cell(world: dict, spatial_grid: dict, grid_x: int, grid_y: int):
	x, y = grid_x * Settings.SPRITES.WIDTH, grid_y * Settings.SPRITES.HEIGHT

	new_id = States.NEXT_ENTITY_ID
	States.NEXT_ENTITY_ID += 1

	artifact = {
		SpacialComponent: SpacialComponent(
			grid_pos=(grid_x, grid_y),
			rect=pygame.Rect(x, y, Settings.SPRITES.WIDTH, Settings.SPRITES.HEIGHT)
			),
		RenderComponent: RenderComponent(
			color=Settings.DEBUG.RAYCAST_COLOR,
			),
	}

	world[new_id] = artifact
	Misc.register_entity_in_grid(new_id, (grid_x, grid_y), spatial_grid)

	return new_id

def spawn_guard(world: dict, spatial_grid: dict, grid_x: int, grid_y: int):
	x, y = grid_x * Settings.SPRITES.WIDTH, grid_y * Settings.SPRITES.HEIGHT

	new_id = States.NEXT_ENTITY_ID
	States.NEXT_ENTITY_ID += 1

	guard = {
		SpacialComponent: SpacialComponent(
			grid_pos= (grid_x, grid_y),
			rect=pygame.Rect(x, y, Settings.SPRITES.WIDTH, Settings.SPRITES.HEIGHT)
		),
		RenderComponent: RenderComponent(color=Settings.DEBUG.PLAYER_COLOR),
		AnimationStateComponent: AnimationStateComponent(state=Enums.ANIM_STATES.IDLE),
		AnimationComponent: AnimationComponent(
			frames=Cache.SPRITES.ENEMY.GUARD,
			current_frame=0,
			state=0,
			direction=Enums.DIRECTIONS.DOWN,
		),
		GuardTag: GuardTag(),
		RayCastComponent: RayCastComponent(length=5, angle_spread=60),
		ObstacleTag: ObstacleTag(),
		PathFindingComponent: PathFindingComponent(),
		AIStateComponent: AIStateComponent(state=Enums.AI_STATES.SEARCH),
	}

	world[new_id] = guard
	Misc.register_entity_in_grid(new_id, (grid_x, grid_y), spatial_grid)

	return new_id

def spawn_extraction_point(world: dict, spatial_grid: dict, grid_x: int, grid_y: int, action: Callable):
	x, y = grid_x * Settings.SPRITES.WIDTH, grid_y * Settings.SPRITES.HEIGHT

	new_id = States.NEXT_ENTITY_ID
	States.NEXT_ENTITY_ID += 1

	artifact = {
		SpacialComponent: SpacialComponent(
			grid_pos=(grid_x, grid_y),
			rect=pygame.Rect(x, y, Settings.SPRITES.WIDTH, Settings.SPRITES.HEIGHT)
			),
		RenderComponent: RenderComponent(
			color=Settings.DEBUG.ARTIFACT_COLOR,
			sprite=Cache.SPRITES.EXTRACTION_POINT_MARKER
			),
		ExtractionTag: ExtractionTag(),
		InteractableComponent: InteractableComponent(layer=ExtractionTag, action=action)
	}

	world[new_id] = artifact
	Misc.register_entity_in_grid(new_id, (grid_x, grid_y), spatial_grid)

	return new_id

def new_button(ui: dict, text: str, center: tuple = (0, 0), size: tuple = (0, 0)):
	new_id = States.NEXT_UI_ELEMENT_ID
	States.NEXT_UI_ELEMENT_ID += 1

	rect = pygame.Rect((0, 0), size)
	rect.center = center

	button = {
		SpacialComponent: SpacialComponent(rect=rect),
		BackgroundComponent: BackgroundComponent(color=Settings.UI.BUTTON_COLOR),
		HoverComponent: HoverComponent(normal_color=Settings.UI.BUTTON_COLOR, hovered_color=Settings.UI.HOVERED_BUTTON_COLOR),
		ClickableComponent: ClickableComponent(),
		TextComponent: TextComponent(text=text.upper().upper(), color=Settings.UI.TEXT_COLOR)
	}

	ui[new_id] = button

	return new_id

def new_panel(ui: dict, center: tuple = (0, 0), size: tuple = (0, 0)):
	new_id = States.NEXT_UI_ELEMENT_ID
	States.NEXT_UI_ELEMENT_ID += 1

	rect = pygame.Rect((0, 0), size)
	rect.center = center

	panel = {
		SpacialComponent: SpacialComponent(rect=rect),
		BackgroundComponent: BackgroundComponent(color=Settings.UI.PANEL_COLOR),
	}

	ui[new_id] = panel

	return new_id

def label(ui: dict, text: str, center: tuple = (0, 0), size: tuple = (0, 0)):
	new_id = States.NEXT_UI_ELEMENT_ID
	States.NEXT_UI_ELEMENT_ID += 1

	rect = pygame.Rect((0, 0), size)
	rect.center = center

	label = {
		SpacialComponent: SpacialComponent(rect=rect),
		BackgroundComponent: BackgroundComponent(color=Settings.UI.BUTTON_COLOR),
		TextComponent: TextComponent(text=text.upper(), color=Settings.UI.TEXT_COLOR)
	}

	ui[new_id] = label

	return new_id