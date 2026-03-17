from dataclasses import dataclass
from pygame import Rect

@dataclass
class SpacialComponent:
	rect: Rect

@dataclass
class RenderComponent:
	color: tuple

class PlayerInputTag: pass