import sys
from enum import Enum

class Neighbor():
    def __init__(self, piece = None, diff = sys.float_info.max):
        self.piece = piece
        self.diff = diff

class Side(Enum):
    LEFT = 1
    RIGHT = 2
    BOTTOM = 3
    TOP = 4