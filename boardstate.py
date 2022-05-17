from enum import Enum

# The board is defined with size N * N
N = 15

class BoardState(Enum):
	#three possible states for a given intersection
    EMPTY = 0
    BLACK = 1
    WHITE = 2