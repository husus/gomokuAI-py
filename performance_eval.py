from AI import *
import math
import time
from copy import deepcopy
import pandas as pd

moves_list = [  (7,7), (8,8),\
                (8,6), (6,8),\
                (7,8), (7,9),\
                (7,5), (9,7),\
                (7,6), (7,4),\
                (10,6), (9,6),\
                (9,5), (8,5),\
                (10,7), (8,10)
                # (10,4), (11,3)
                ]

#initialized GomokuAI object in order to create a board
AI = GomokuAI()


def board_to_eval(ai, moves):

    ai.currentState =  1 #AI starts first (CAN be changed)
    board_value = 0

    for m in moves:
        bound = ai.nextBound
        turn = ai.currentState

        ai.boardValue = ai.evaluate(m[0], m[1], board_value, -1, bound)
        ai.setState(m[0], m[1], turn)
        ai.currentI, ai.currentJ = m[0], m[1]
        ai.updateBound(m[0], m[1], bound)
        ai.emptyCells -= 1
        # ai.drawBoard()
        ai.currentState *= -1

def ai_runtime(ai):
    board_to_eval(ai, moves_list)
    runtime = []
    moves_chosen = []

    for i in range(1,7):
        new_ai = deepcopy(ai)
        start_time = time.time()
        new_ai.alphaBetaPruning(i, new_ai.boardValue, new_ai.nextBound, -math.inf, math.inf, True)
        end_time = time.time()
        time_diff = end_time - start_time
        runtime.append(time_diff)

        moves_chosen.append((new_ai.currentI, new_ai.currentJ))
        print('Done {} in {}'.format(i, time_diff))
    
    return runtime, moves_chosen


if __name__ == '__main__':
    runtime, moves_chosen = ai_runtime(AI)
    df = pd.DataFrame(
        {'runtime': runtime,
        'moves_chosen': moves_chosen
    })
    df.to_csv('performance_eval.csv')
    print(runtime, moves_chosen)

