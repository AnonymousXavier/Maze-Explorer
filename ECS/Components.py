from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Optional, Any
import pygame

@dataclass(kw_only=True)
class SpacialComponent:
	grid_pos: Optional[tuple] = None
	rect: pygame.Rect

@dataclass(kw_only=True)
class RenderComponent:
	color: tuple
	sprite: Optional[pygame.Surface] = None
	z_index: int = 0

@dataclass(kw_only=True)
class StalkerComponent:
	target_id: int

@dataclass(kw_only=True)
class AnimationStateComponent:
	state: int

@dataclass(kw_only=True)
class AIStateComponent:
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

@dataclass(kw_only=True)
class PathFindingComponent:
	path: Optional[list] = field(default_factory=list)

@dataclass(kw_only=True)
class InteractableComponent:
	layer: Any # Type of object it is, so it can be found by another with a matching mask
	one_time: Optional[bool] = True # Should Delete after interaction
	action: Optional[Callable]

@dataclass(kw_only=True)
class InteractorComponent:
	mask: Any # Like Entities or Chests -> What the object will look for


class PlayerInputTag: pass
class ArtifactTag: pass
class ObstacleTag: pass
class FloorTag: pass
class GuardTag: pass
class ExtractionTag: pass

# UI
@dataclass(kw_only=True)
class BackgroundComponent:
	color: tuple

@dataclass(kw_only=True)
class HoverComponent:
	normal_color: tuple
	hovered_color: tuple

@dataclass(kw_only=True)
class ClickableComponent:
	clicked: Optional[bool] = False
	action: Callable

@dataclass(kw_only=True)
class TextComponent:
	text: str
	color: tuple
	
@dataclass(kw_only=True)
class ImageComponent:
	sprite: pygame.Surface

class MainMenuElementTag: pass
class GameOverElementTag: pass
class SuccessMenuElementTag: pass
class GameUIElementTag: pass