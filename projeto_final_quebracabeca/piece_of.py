from neighbor import Neighbor, Side
import uuid

class Piece:
    def __init__(self, content, done = False):
        self.content = content
        self.neighbors = {
            Side.LEFT: Neighbor(),
            Side.RIGHT: Neighbor(),
            Side.BOTTOM: Neighbor(),
            Side.TOP: Neighbor(),
        }

    def has_neighbor(self, side):
        return self.neighbors[side] != None and self.neighbors[side].piece != None