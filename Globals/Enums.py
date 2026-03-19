from enum import Enum


class CELL_ELEMENTS(Enum):
	EMPTY = 0
	WALL = 1
	DOOR = 2

class EventType(Enum):
	MOVEMENT_INTENT = 0

class INTERPOLATION(Enum):
	LINEAR = 0
	EASE_OUT = 1