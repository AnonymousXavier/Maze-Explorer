import pygame
from math import sin, radians, cos

BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

w, h = size = 600, 600
c, r = 1001, 1001
cw, ch = w / c, h / r

pxi, pyi = c // 2, r // 2
window = pygame.display.set_mode(size)
grid: dict[tuple, tuple] = {}

for yi in range(r):
	for xi in range(c):
		grid[(xi, yi)] = BLUE


rect = pygame.Rect(pxi * cw, pyi * ch, cw, ch)
pygame.draw.rect(window, RED, rect)

facing_direction = 0
length = c // 5
angle_spread = 45

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()

	# Update RayCast Colors
	min_angle = facing_direction % 360 - angle_spread // 2
	max_angle = facing_direction % 360 + angle_spread // 2

	for yi in range(r):
		for xi in range(c):
			grid[(xi, yi)] = BLUE

	for angle in range(min_angle, max_angle + 1):
		arc_length = length
		while arc_length > 0:
			xi = round(cos(radians(angle)) * arc_length)
			yi = round(sin(radians(angle)) * arc_length)

			grid[(pxi + xi, pyi + yi)] = GREEN

			arc_length -= 1

	for (xi, yi) in grid:
		color = grid[(xi, yi)]
		rect = pygame.Rect(xi * cw, yi * ch, cw, ch)
		pygame.draw.rect(window, color, rect)

	pygame.display.update()

	facing_direction += 1





