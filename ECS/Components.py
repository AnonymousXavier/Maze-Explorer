from dataclasses import dataclass, field
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

@dataclass(kw_only=True)
class RayCastComponent:
	facing_direction: Optional[int] = -90  # angle, -90 is up, 0 is right
	length: int
	angle_spread: int # Angle of the arc

@dataclass(kw_only=True)
class RayCastRegion:
	points: set = field(default_factory=set)
	found_entities: set = field(default_factory=set)
	shape: Optional[tuple] = ()
	pivot: Optional[tuple] = -1, -1
	size: Optional[pygame.Surface] = None

class PlayerInputTag: pass
class ArtifactTag: pass
class ObstacleTag: pass
class FloorTag: pass
class GuardTag: pass