from ECS.Components import ObstacleTag, SpacialComponent
from Globals import Enums, Settings, Misc

interpolating_objects = {}

frame = 0

def process(world: dict, spatial_grid: dict, global_event: list, delta: float):
    global frame

    if frame % (Settings.WINDOW.FPS / Settings.WINDOW.INPUTS_CHECKS_PER_SEC) == 0:
        for event in global_event:
            hit_a_wall = False

            if event["type"] == Enums.EventType.MOVEMENT_INTENT:
                obj_id = event["entity_id"] 
                if SpacialComponent in world[obj_id]:
                    obj = world[obj_id]

                    gx, gy = obj[SpacialComponent].grid_pos
                    dx, dy = event["dx"], event["dy"]
                    nx, ny = (gx + dx, gy + dy)

                    if (nx, ny) in spatial_grid:
                        for _obj_id in spatial_grid[(nx, ny)]:
                            if ObstacleTag in world[_obj_id]:
                                hit_a_wall = True
                                break

                    if hit_a_wall: break

                    obj_rect = world[obj_id][SpacialComponent].rect
                    tx, ty = nx * Settings.SPRITES.WIDTH, ny * Settings.SPRITES.HEIGHT

                    interpolating_objects[obj_id] = {"position": obj_rect.topleft, "target": (tx, ty), "delta": delta}

                    move_entity_on_spatial_grid(obj_id, (nx, ny), world, spatial_grid)

    # Interpolate Movements
    objects_done_with_interpolation = []
    for obj_id in interpolating_objects:
        px, py = interpolating_objects[obj_id]["position"]
        tx, ty = interpolating_objects[obj_id]["target"]
        delta = interpolating_objects[obj_id]["delta"]

        dx, dy = tx - px, ty - py

        if dx == 0 and dy == 0:
            world[obj_id][SpacialComponent].rect.topleft = tx, ty
            objects_done_with_interpolation.append(obj_id)
            continue 

        interpolating_objects[obj_id]["position"] = Misc.move_towards((px, py), (tx, ty), Settings.GAME.PLAYER_SPEED * delta)
        world[obj_id][SpacialComponent].rect.topleft = interpolating_objects[obj_id]["position"]

    for obj_id in objects_done_with_interpolation:
        del interpolating_objects[obj_id]

    frame += 1

def move_entity_on_spatial_grid(entity_id: int, new_position: tuple, world:dict, spatial_grid: dict):
    obj = world[entity_id]
    old_pos = obj[SpacialComponent].grid_pos

    Misc.remove_entity_from_grid(entity_id, old_pos, spatial_grid)
    Misc.register_entity_in_grid(entity_id, new_position, spatial_grid)

    obj[SpacialComponent].grid_pos = new_position

