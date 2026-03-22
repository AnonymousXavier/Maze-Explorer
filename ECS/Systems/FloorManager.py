from ECS import Factories
from ECS.Components import SpacialComponent
from ECS.Systems import CameraSystem
from Globals import Cache, Settings, Misc

floor_id = 0

def spawn_floor(world: dict, spatial_grid: dict, camera: dict, grid_x, grid_y):
	global floor_id

	cam_boundary = CameraSystem.get_boundary_of(camera)

	sx, sy = Cache.tileset_dict["floor"]
	sprite = Cache.SPRITES.TILESET[sy][sx]
	floor_id = Factories.generate_and_spawn_floor_sprite(world, spatial_grid, cam_boundary, grid_x, grid_y, sprite)

def process(world: dict, spatial_grid: dict, camera: dict):
	# Keep floor in drawable region
	cam_boundary = CameraSystem.get_boundary_of(camera)
	cam_left, cam_top = cam_boundary["left"], cam_boundary["top"]

	floor_obj = world[floor_id]
	old_pos = floor_obj[SpacialComponent].grid_pos
	floor_obj[SpacialComponent].grid_pos = (cam_left, cam_top)

	Misc.remove_entity_from_grid(floor_id, old_pos, spatial_grid)
	Misc.register_entity_in_grid(floor_id, (cam_left, cam_top), spatial_grid)

	floor_obj[SpacialComponent].rect.topleft = (cam_left - 1)  * Settings.SPRITES.WIDTH, (cam_top - 1) * Settings.SPRITES.HEIGHT
