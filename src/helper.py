from random import shuffle


def get_next_positions(board):
    """Return a list of allowed positions for the given board state."""

    next_positions = [i for i, p in enumerate(board) if p == 0]
    shuffle(next_positions)
    return next_positions


def get_winner(board):
    """Return winner (`1` or `2`) for the given board state.

    `0` for draw and `None` if the game is not over yet.
    """

    # Horizontal check
    for i in [0, 3, 6]:
        if board[i] == board[i+1] and board[i+1] == board[i+2]:
            if board[i] == 1:
                return 1
            elif board[i] == 2:
                return 2

    # Vertical check
    for i in range(3):
        if board[i] == board[i+3] and board[i+3] == board[i+6]:
            if board[i] == 1:
                return 1
            elif board[i] == 2:
                return 2

    # Diagonal check
    if board[0] == board[4] and board[4] == board[8]:
        if board[0] == 1:
            return 1
        elif board[0] == 2:
            return 2

    if board[2] == board[4] and board[4] == board[6]:
        if board[2] == 1:
            return 1
        elif board[2] == 2:
            return 2

    if not get_next_positions(board):
        return 0

    return None


def minimax(board, depth, max_turn, alpha, beta, maximizer, minimizer):
    evaluate = {None: 0, 0: 0, maximizer: 1, minimizer: -1}
    score = evaluate[get_winner(board)]
    next_positions = get_next_positions(board)

    if score == 1 or score == -1:
        return score

    if get_winner(board) == 0:
        return 0

    if max_turn:
        best = -1000
        for position in next_positions:
            board[position] = maximizer
            best = max(best, minimax(board, depth-1, not max_turn,
                       alpha, beta, maximizer, minimizer))
            board[position] = 0

            alpha = max(alpha, best)
            if alpha >= beta or depth == 0:
                break

        return best
    else:
        best = 1000
        for position in next_positions:
            board[position] = minimizer

            best = min(best, minimax(board, depth-1, not max_turn,
                       alpha, beta, maximizer, minimizer))

            board[position] = 0

            beta = min(beta, best)
            if alpha >= beta or depth == 0:
                break

        return best


def get_best_position(board, maximizer, minimizer,  cache, depth):
    """Return best position for the given board state.

    `depth`: Depth limit for minimax search.
    """

    if str(board) in cache:
        return cache[str(board)]

    best_value = -1000
    best_position = None

    for position in get_next_positions(board):
        board[position] = maximizer

        position_value = minimax(
            board[:], depth, False, -1000, 1000, maximizer, minimizer)

        board[position] = 0

        if position_value > best_value:
            best_value = position_value
            best_position = position

    cache[str(board)] = best_position

    return best_position
