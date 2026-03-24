import pygame
import math

def create_cone_sprite(radius, facing_direction, angle_spread, accuracy=1):
    """
    Generates a standalone Pygame surface containing a raycasting cone.
    
    radius: Length of the cone in pixels.
    facing_direction: Center angle of the cone in degrees.
    angle_spread: Total width of the cone in degrees.
    accuracy: Step size in degrees. Lower = smoother visual arc.
    """
    
    # 1. The Fixed Bounding Box
    # A square that can contain the cone at any rotation
    surface_size = int(2 * radius)
    
    # SRCALPHA ensures the background of the square is fully transparent
    cone_surface = pygame.Surface((surface_size, surface_size), pygame.SRCALPHA)
    
    # 2. The Fixed Origin
    # The tip of the cone is permanently locked to the center of the surface
    cx, cy = radius, radius
    
    # 3. Calculate Angles
    min_angle = facing_direction - (angle_spread / 2)
    max_angle = facing_direction + (angle_spread / 2)
    
    # 4. Generate Polygon Points
    points = [(cx, cy)]
    current_angle = min_angle
    
    while current_angle <= max_angle:
        rad = math.radians(current_angle)
        
        # Calculate x and y relative to the center of our surface
        x = cx + (radius * math.cos(rad))
        y = cy + (radius * math.sin(rad))
        
        points.append((x, y))
        current_angle += accuracy
        
    # 5. Draw to the Surface
    # Using RGBA for a semi-transparent yellow "light" or "vision" cone
    cone_color = (255, 255, 0, 100) 
    pygame.draw.polygon(cone_surface, cone_color, points)
    
    return cone_surface
