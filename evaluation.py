from boardstate import *

WHITE_6PATTERNS = [['.', 'o', 'o', 'o', 'o','.'],
                ['.', 'o', 'o', 'o', '.','.'],
                ['.', '.', 'o', 'o', 'o','.'],
                ['.', 'o', 'o', '.', 'o','.'],
                ['.', 'o', '.', 'o', 'o','.'],
                ['.', '.', 'o', 'o', '.','.'],
                ['.', '.', 'o', '.', 'o','.'],
                ['.', 'o', '.', 'o', '.','.'],
                ['.', '.', 'o', '.', '.','.'],
                ['.', '.', '.', 'o', '.','.']]

WHITE_6SCORES = [50000,5000,5000,500,500,100,100,100,10,10]
# o_6SCORES = [8640,720,720,720,720,120,120,120,20,20] #based on Dong (2015)


WHITE_5PATTERNS = [['o', 'o', 'o', 'o', 'o'],
                ['o', 'o', 'o', 'o', '.'],
                ['.', 'o', 'o', 'o', 'o'],
                ['o', 'o', '.', 'o', 'o'],
                ['o', '.', 'o', 'o', 'o'],
                ['o', 'o', 'o', '.', 'o']]
WHITE_5SCORES = [1000000,5000,5000,5000,5000,5000]
# o_5SCORES = [50000,720,720,720,720,720] #based on Dong (2015)

BLACK_6PATTERNS = [['.', 'x', 'x', 'x', 'x','.'],
                ['.', 'x', 'x', 'x', '.','.'],
                ['.', '.', 'x', 'x', 'x','.'],
                ['.', 'x', 'x', '.', 'x','.'],
                ['.', 'x', '.', 'x', 'x','.'],
                ['.', '.', 'x', 'x', '.','.'],
                ['.', '.', 'x', '.', 'x','.'],
                ['.', 'x', '.', 'x', '.','.'],
                ['.', '.', 'x', '.', '.','.'],
                ['.', '.', '.', 'x', '.','.']]
BLACK_6SCORES = [50000,5000,5000,500,500,100,100,100,10,10]
# x_6SCORES = [8640,720,720,720,720,120,120,120,20,20] #based on Dong (2015)


BLACK_5PATTERNS = [['x', 'x', 'x', 'x', 'x'],
                ['x', 'x', 'x', 'x', '.'],
                ['.', 'x', 'x', 'x', 'x'],
                ['x', 'x', '.', 'x', 'x'],
                ['x', '.', 'x', 'x', 'x'],
                ['x', 'x', 'x', '.', 'x']]
BLACK_5SCORES = [1000000,5000,5000,5000,5000,5000]


def enum_to_string(vector):
    '''
    Change BoardState.WHITE to 'white'.
    '''
    string_list = []
    for item in vector:
        if item == BoardState.BLACK:
            string_list.append('x')
        elif item == BoardState.WHITE:
            string_list.append('o')
        else:
            string_list.append('.')
    
    return string_list


def evaluate_vector(vector):
    '''
    Return the score for a vector (line or column or diagonal)
    '''
    string_list = enum_to_string(vector)
    score = {'white': 0, 'black': 0}
    length = len(string_list)

    if length == 5:
        for i in range(len(WHITE_5PATTERNS)):
            if WHITE_5PATTERNS[i] == string_list:
                score['white'] += WHITE_5SCORES[i]
            if BLACK_5PATTERNS[i] == string_list:
                score['black'] += BLACK_5SCORES[i]
        return score

    for i in range(length - 5):
        temp = [string_list[i], string_list[i + 1], string_list[i + 2],
                string_list[i + 3], string_list[i + 4]]
        for i in range(len(WHITE_5PATTERNS)):
            if WHITE_5PATTERNS[i] == temp:
                score['white'] += WHITE_5SCORES[i]
            if BLACK_5PATTERNS[i] == temp:
                score['black'] += BLACK_5SCORES[i]

    for i in range(length - 6):
        temp = [
            string_list[i],
            string_list[i + 1],
            string_list[i + 2],
            string_list[i + 3],
            string_list[i + 4],
            string_list[i + 5],
            ]
        for i in range(len(WHITE_6PATTERNS)):
            if WHITE_6PATTERNS[i] == temp:
                score['white'] += WHITE_6SCORES[i]
            if BLACK_6PATTERNS[i] == temp:
                score['black'] += BLACK_6SCORES[i]
    return score

def create_pattern_dict():
    x = -1
    patternDict = {}
    while (x < 2):
        y = -x
        # long_5
        patternDict[(x, x, x, x, x)] = 1000000 * x
        # live_4
        patternDict[(0, x, x, x, x, 0)] = 1000 * x
        # go_4
        patternDict[(0, x, x, x, x, y)] = 500 * x
        patternDict[(y, x, x, x, x, 0)] = 500 * x
        patternDict[(0, x, x, x, 0, x, 0)] = 500 * x
        patternDict[(0, x, 0, x, x, x, 0)] = 500 * x
        patternDict[(0, x, x, 0, x, x, 0)] = 500 * x
        # dead_4
        patternDict[(y, x, x, x, x, y)] = -5 * x
        # live_3
        patternDict[(0, x, x, x, 0)] = 200 * x
        patternDict[(0, x, 0, x, x, 0)] = 200 * x
        patternDict[(0, x, x, 0, x, 0)] = 200 * x
        # sleep_3
        patternDict[(0, 0, x, x, x, y)] = 50 * x
        patternDict[(y, x, x, x, 0, 0)] = 50 * x
        patternDict[(0, x, 0, x, x, y)] = 50 * x
        patternDict[(y, x, x, 0, x, 0)] = 50 * x
        patternDict[(0, x, x, 0, x, y)] = 50 * x
        patternDict[(y, x, 0, x, x, 0)] = 50 * x
        patternDict[(x, 0, 0, x, x)] = 50 * x
        patternDict[(x, x, 0, 0, x)] = 50 * x
        patternDict[(x, 0, x, 0, x)] = 50 * x
        patternDict[(y, 0, x, x, x, 0, y)] = 50 * x
        # dead_3
        patternDict[(y, x, x, x, y)] = -5 * x
        # live_2
        patternDict[(0, 0, x, x, 0)] = 5 * x
        patternDict[(0, x, x, 0, 0)] = 5 * x
        patternDict[(0, x, 0, x, 0)] = 5 * x
        patternDict[(0, x, 0, 0, x, 0)] = 5 * x
        # sleep_2
        patternDict[(0, 0, 0, x, x, y)] = 3 * x
        patternDict[(y, x, x, 0, 0, 0)] = 3 * x
        patternDict[(0, 0, x, 0, x, y)] = 3 * x
        patternDict[(y, x, 0, x, 0, 0)] = 3 * x
        patternDict[(0, x, 0, 0, x, y)] = 3 * x
        patternDict[(y, x, 0, 0, x, 0)] = 3 * x
        patternDict[(x, 0, 0, 0, x)] = 3 * x
        patternDict[(y, 0, x, 0, x, 0, y)] = 3 * x
        patternDict[(y, 0, x, x, 0, 0, y)] = 3 * x
        patternDict[(y, 0, 0, x, x, 0, y)] = 3 * x
        # dead_2
        patternDict[(y, x, x, y)] = -5 * x
        x += 2
    return patternDict

def transform_pattern(patternDict):
    new_patternDict = {}
    for k,v in patternDict.items():
        pattern = []
        for i in k:
            if i == 0:
                i = '.'
            if i == 1:
                i = 'x'
            if i == -1:
                i = 'o'
            pattern.append(i)
        pattern = tuple(pattern)
        new_patternDict[pattern] = patternDict[k]
    return new_patternDict