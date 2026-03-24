from ECS.Components import ObstacleTag, SpacialComponent
from Globals import Settings

def get_path_to_obj(world: dict, spatial_grid: dict, obj_id: int, target_id: int):
    start_pos = world[obj_id][SpacialComponent].grid_pos
    stop_pos  = world[target_id][SpacialComponent].grid_pos

    return find_path_bfs(world, spatial_grid, start_pos, stop_pos, Settings.MAP.WORLD_SIZE)

def find_path_bfs(world: dict, spatial_grid: dict, start_pos: tuple, target_pos: tuple, map_size: tuple) -> list:
    from collections import deque

    if start_pos == target_pos:
        return []

    max_x, max_y = map_size

    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    queue = deque([start_pos])
    visited = set([start_pos])
    came_from = {}

    def in_bounds(pos):
        x, y = pos
        return 0 <= x < max_x and 0 <= y < max_y

    def is_walkable(pos):
        if not in_bounds(pos):
            return False

        if pos in spatial_grid:
            for entity_id in spatial_grid[pos]:
                if ObstacleTag in world[entity_id]:
                    return False
        return True

    while queue:
        current = queue.popleft()

        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)

            if neighbor in visited:
                continue

            if not is_walkable(neighbor):
                continue

            visited.add(neighbor)
            came_from[neighbor] = current

            if neighbor == target_pos:
                path = []
                cur = neighbor
                while cur != start_pos:
                    path.append(cur)
                    cur = came_from[cur]
                path.reverse()
                return path

            queue.append(neighbor)

    return []