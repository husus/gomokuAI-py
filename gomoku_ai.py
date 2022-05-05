
# Minimax function
def minimax(position, depth, maximizingPlayer):
    if depth==0: #or end game
        return eval #evaluation of current position
    if maximizingPlayer:
        max_val = float("-inf")
        for child in position:
            eval = minimax(child, depth-1, False)
            max_val = max(max_val, eval)
        return max_val
    else:
        min_val = float("inf")
        for child in position:
            eval = minimax(child, depth-1, True)
            min_val = min(min_val, eval)
        return min_val 


# Minimax function with alpha beta pruning
def ab_pruning(position, depth, alpha, beta, maximizingPlayer):
    if depth==0: #or end game
        return eval #evaluation of current position
    if maximizingPlayer:
        max_val = float("-inf")
        for child in position:
            eval = minimax(child, depth-1, alpha, beta, False)
            max_val = max(max_val, eval)
            alpha = max(alpha, eval)
        return max_val
    else:
        min_val = float("inf")
        for child in position:
            eval = minimax(child, depth-1, alpha, beta, True)
            min_val = min(min_val, eval)
            beta = min(beta, eval)
        return min_val