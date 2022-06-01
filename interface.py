import pygame
import os
from AI import *

SIZE = 540 #size of the board image
PIECE = 32 #size of the single pieces
N = 15
MARGIN = 23
# GRID = 35
GRID = (SIZE - 2 * MARGIN) / (N-1)
# 35x35 size of squares in the board

'''
(23,23) start of internal square --> (7,7)
(517,23) top right end of internal square --> (533,7)
(23,517) bottom left start of internal square --> (7,533)
(517,517) bottom right end of internal square --> (533,533)
'''


SCREEN = pygame.display.set_mode((SIZE, SIZE))
pygame.display.set_caption('Play Gomoku!')

BG = pygame.image.load(os.path.join("assets", 'board.jpg')).convert() #set board image as bg
BLACK_PIECE = pygame.image.load(os.path.join("assets", 'black_piece.png')).convert_alpha()
# BLACK_PIECE = pygame.transform.scale(BLACK_PIECE,(35,35))

WHITE_PIECE = pygame.image.load(os.path.join("assets", 'white_piece.png')).convert_alpha()
# WHITE_PIECE = pygame.transform.scale(WHITE_PIECE,(35,35))

# FPS = 60 #how many frames per second to update the window

# def grid(screen, size, rows):
#     x = 7
#     y = 7
#     cell = size//rows
#     for l in range(rows):
#         x += cell
#         y += cell
#         pygame.draw.line(screen, (255,255,255), (x,7), (x,size))
#         pygame.draw.line(screen, (255,255,255), (7,y), (size,y))

# def drawGrid():
#     cell = 35 #Set the size of the grid block
#     for x in range(SIZE-14):
#         for y in range(SIZE-14):
#             rect = pygame.Rect(x*cell+7, y*cell+7,
#                                cell, cell)
#             pygame.draw.rect(SCREEN, (255,255,255), rect, 1)

def draw_window():
    # SCREEN.blit(BG, (0,0))
    # SCREEN.blit(BLACK_PIECE, 
    #         (SIZE/2-PIECE/2, SIZE/2-PIECE/2)) #central position of the black piece
    
    # SCREEN.blit(WHITE_PIECE, 
    #         (517-PIECE/2,23-PIECE/2))
    
    # rect = pygame.Rect(7,7,526,526)
    # pygame.draw.rect(SCREEN, (255,255,255), rect, 2) #create a square for saving moves

    mapping = create_mapping()

    for v in mapping.values():
        x = v[0] - PIECE/2
        y = v[1] - PIECE/2
        SCREEN.blit(WHITE_PIECE, (x, y))

    pygame.display.update()

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

def draw_piece(state, mapping, i, j):
    # (x, y) = pygame.mouse.get_pos()

    x, y = mapping[(i,j)]
    x = x - PIECE/2
    y = y - PIECE/2

    if state == 1: #TODO: change to black
        SCREEN.blit(BLACK_PIECE, (x, y))
    
    elif state == -1: #TODO: change to white
        SCREEN.blit(WHITE_PIECE, (x, y))

    pygame.display.update()
    
def draw_result():
    pass

def main():
    pygame.init()
    # clock = pygame.time.Clock()
    run = True
    SCREEN.blit(BG, (0,0))
    pygame.display.update()
    state = 1
    pos_mapping = create_mapping()

    while run:
        # clock.tick(FPS) #to control the speed of while loop, never go over that speed
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    print(pos)
                    (i, j) = pos_pixel2map(pos[0], pos[1])
                    print((i,j))
                    # x, y = pos_map2pixel(i,j)
                    # # x -= PIECE / 2
                    # # y -= PIECE / 2
        
                    draw_piece(state, pos_mapping, i,j)
                    # pygame.display.update()
                    state *= -1
        # draw_window()
        # pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()