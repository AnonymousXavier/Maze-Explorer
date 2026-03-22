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
	z_index: int = 0

@dataclass(kw_only=True)
class StalkerComponent:
	target_id: int

@dataclass(kw_only=True)
class StateComponent:
	state: int

@dataclass(kw_only=True)
class AnimationComponent:
	frames: dict
	current_frame: int
	state: int
	direction: int

@dataclass(kw_only=True)
class VelocityComponent:
	position: tuple
	target: tuple
	speed: float

class PlayerInputTag: pass
class ObstacleTag: pass
class FloorTag: pass