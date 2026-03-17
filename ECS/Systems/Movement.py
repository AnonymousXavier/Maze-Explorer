from ECS.Components import SpacialComponent
from Globals import Enums, Settings

def process(world: dict, global_event: list):
    for event in global_event:
        if event["type"] == Enums.EventType.MOVEMENT_INTENT:
            obj_id = event["entity_id"] 
            if SpacialComponent in world[obj_id]:
                dx, dy = event["dx"], event["dy"]
                obj_rect = world[obj_id][SpacialComponent].rect

                obj_rect.x += dx * Settings.SPRITES.WIDTH
                obj_rect.y += dy * Settings.SPRITES.HEIGHT