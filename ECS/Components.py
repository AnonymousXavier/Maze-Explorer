from dataclasses import dataclass
from typing import Optional
from pygame import Rect
import pygame

@dataclass(kw_only=True)
class SpacialComponent:
	grid_pos: Optional[tuple] = None
	rect: Rect

@dataclass(kw_only=True)
class RenderComponent:
	color: tuple
	sprite: Optional[pygame.Surface] = None
	z_index = 0

@dataclass(kw_only=True)
class StalkerComponent:
	target_id: Optional[int] = None


class PlayerInputTag: pass
class ObstacleTag: pass