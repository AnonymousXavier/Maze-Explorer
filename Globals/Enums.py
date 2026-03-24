from enum import Enum


class CELL_ELEMENTS(Enum):
	EMPTY = 0
	WALL = 1
	DOOR = 2

class EventType(Enum):
	MOVEMENT_INTENT = 0
	SEARCH_INTENT = 1
	PATHFIND_INTENT = 2

class INTERPOLATION(Enum):
	LINEAR = 0
	EASE_OUT = 1

class ANIM_STATES:
	WALK = 0
	IDLE = 1
	DEAD = 2

class DIRECTIONS:
	UP = 1
	DOWN = 0
	LEFT = 2
	RIGHT = 3

	ALL = (DOWN, RIGHT, UP, LEFT)