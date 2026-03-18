from ECS.Components import SpacialComponent
from Globals import Enums, Settings, Misc

def process(world: dict, spatial_grid: dict, global_event: list):
    for event in global_event:
        if event["type"] == Enums.EventType.MOVEMENT_INTENT:
            obj_id = event["entity_id"] 
            if SpacialComponent in world[obj_id]:
                obj = world[obj_id]

                gx, gy = obj[SpacialComponent].grid_pos
                dx, dy = event["dx"], event["dy"]
                obj_rect = world[obj_id][SpacialComponent].rect

                obj_rect.x += dx * Settings.SPRITES.WIDTH
                obj_rect.y += dy * Settings.SPRITES.HEIGHT

                move_entity_on_spatial_grid(obj_id, (gx + dx, gy + dy), world, spatial_grid)


def move_entity_on_spatial_grid(entity_id: int, new_position: tuple, world:dict, spatial_grid: dict):
    obj = world[entity_id]
    old_pos = obj[SpacialComponent].grid_pos

    Misc.remove_entity_from_grid(entity_id, old_pos, spatial_grid)
    Misc.register_entity_in_grid(entity_id, new_position, spatial_grid)

    obj[SpacialComponent].grid_pos = new_position

