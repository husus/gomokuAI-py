import random
import uuid

##### For managing the interface #####
SIZE = 540 #size of the board image
PIECE = 32 #size of the single pieces
N = 15
MARGIN = 23
GRID = (SIZE - 2 * MARGIN) / (N-1)

def pixel_conversion(list_points, target):
    # point of the list from where start the search
    index = int((len(list_points)-1)//2) 

    while True:
        if target < list_points[0]:
            index = 0
            break
        elif target >= list_points[-1]:
            index = len(list_points)-2
            break

        elif list_points[index] > target:
            if list_points[index-1] <= target:
                index -= 1
                break
            else:
                index -= 1

        elif list_points[index] <= target:
            if list_points[index+1] > target:
                break
            else:
                index += 1
    
    return index

def pos_pixel2map(x, y):
    # transform pygame pixel to boardMap coordinates

    start = int(MARGIN - GRID//2)
    end = int(SIZE - MARGIN + GRID//2)
    list_points = [p for p in range(start, end+1, int(GRID))]

    i = pixel_conversion(list_points, y)
    j = pixel_conversion(list_points, x)
    return (i,j)

def pos_map2pixel(i, j):
    # transform boardMap to pygame pixel coordinates
    return (MARGIN + j * GRID - PIECE/2, MARGIN + i * GRID - PIECE/2)

def create_mapping():
    pos_mapping = {}
    for i in range(N):
        for j in range(N):
            spacing = [r for r in range(MARGIN, SIZE-MARGIN+1, int(GRID))]
            pos_mapping[(i,j)] = (spacing[j],spacing[i])
    
    return pos_mapping



##### Pattern scores #####
def create_pattern_dict():
    x = -1
    patternDict = {}
    while (x < 2):
        y = -x
        # long_5
        patternDict[(x, x, x, x, x)] = 1000000 * x
        # live_4
        patternDict[(0, x, x, x, x, 0)] = 50000 * x
        # go_4
        patternDict[(0, x, x, x, x, y)] = 10000 * x
        patternDict[(y, x, x, x, x, 0)] = 10000 * x
        patternDict[(0, x, x, x, 0, x, 0)] = 10000 * x
        patternDict[(0, x, 0, x, x, x, 0)] = 10000 * x
        patternDict[(0, x, x, 0, x, x, 0)] = 10000 * x
        # dead_4
        patternDict[(y, x, x, x, x, y)] = -50 * x
        # live_3
        patternDict[(0, x, x, x, 0)] = 5000 * x
        patternDict[(0, x, 0, x, x, 0)] = 5000 * x
        patternDict[(0, x, x, 0, x, 0)] = 5000 * x
        # sleep_3
        patternDict[(0, 0, x, x, x, y)] = 500 * x
        patternDict[(y, x, x, x, 0, 0)] = 500 * x
        patternDict[(0, x, 0, x, x, y)] = 500 * x
        patternDict[(y, x, x, 0, x, 0)] = 500 * x
        patternDict[(0, x, x, 0, x, y)] = 500 * x
        patternDict[(y, x, 0, x, x, 0)] = 500 * x
        patternDict[(x, 0, 0, x, x)] = 500 * x
        patternDict[(x, x, 0, 0, x)] = 500 * x
        patternDict[(x, 0, x, 0, x)] = 500 * x
        patternDict[(y, 0, x, x, x, 0, y)] = 500 * x
        # dead_3
        patternDict[(y, x, x, x, y)] = -50 * x
        # live_2
        patternDict[(0, 0, x, x, 0)] = 100 * x
        patternDict[(0, x, x, 0, 0)] = 100 * x
        patternDict[(0, x, 0, x, 0)] = 100 * x
        patternDict[(0, x, 0, 0, x, 0)] = 100 * x
        # sleep_2
        patternDict[(0, 0, 0, x, x, y)] = 50 * x
        patternDict[(y, x, x, 0, 0, 0)] = 50 * x
        patternDict[(0, 0, x, 0, x, y)] = 50 * x
        patternDict[(y, x, 0, x, 0, 0)] = 50 * x
        patternDict[(0, x, 0, 0, x, y)] = 50 * x
        patternDict[(y, x, 0, 0, x, 0)] = 50 * x
        patternDict[(x, 0, 0, 0, x)] = 50 * x
        patternDict[(y, 0, x, 0, x, 0, y)] = 50 * x
        patternDict[(y, 0, x, x, 0, 0, y)] = 50 * x
        patternDict[(y, 0, 0, x, x, 0, y)] = 50 * x
        # dead_2
        patternDict[(y, x, x, y)] = -50 * x
        x += 2
    return patternDict



##### Zobrist Hashing #####
def init_zobrist():
    zTable = [[[uuid.uuid4().int  for _ in range(2)] \
                        for j in range(15)] for i in range(15)] #changed to 32 from 64
    return zTable

# def zobrist_hash(i, j, zTable):
#     # hash = 0
#     # for i in range(15):
#     #     for j in range(15):
#     #         if board[i][j] != 0:
#     #             piece = 0 if board[i][j]==1 else 1
#     h ^= zTable[i][j][piece]
    return h

def update_TTable(table, hash, score, depth):
    table[hash] = [score, depth]
