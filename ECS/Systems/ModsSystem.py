from Misc.Mods_Manager import ModsManager

def process(world: dict, spatial_grid: dict, events: list, dt: float):
    # This system loops through every active mod and lets them touch the ECS data
    for mod in ModsManager.active_mods:
        mod.on_update(world, spatial_grid, events, dt)