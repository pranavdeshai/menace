from random import shuffle

cache = {}
winning_positions = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)
similar_positions = (
    (0, 1, 2, 3, 4, 5, 6, 7, 8),
    (2, 5, 8, 1, 4, 7, 0, 3, 6),  # Rotate 90 degrees anti-clockwise
    (8, 7, 6, 5, 4, 3, 2, 1, 0),  # Rotate 180 degrees anti-clockwise
    (6, 3, 0, 7, 4, 1, 8, 5, 2),  # Rotate 270 degrees anti-clockwise
    (2, 1, 0, 5, 4, 3, 8, 7, 6),  # Flip horizontally
    (6, 7, 8, 3, 4, 5, 0, 1, 2),  # Flip vertically
    (0, 3, 6, 1, 4, 7, 2, 5, 8),  # Transpose-1
    (8, 5, 2, 7, 4, 1, 6, 3, 0),  # Transpose-2
)


def get_next_moves(board):
    """Return a list of allowed moves for the given board state."""

    return [i for i, p in enumerate(board) if p == 0]


def get_winner(board):
    """Return the winner for the given board state."""

    for i, j, k in winning_positions:
        if board[i] != 0 and board[i] == board[j] and board[j] == board[k]:
            return board[i]

    if board.count(0) == 0:
        return 0

    return None


def get_best_move(board, next_moves, maximizer, minimizer):
    """Return best move for the given board state."""

    # Similar positions
    for x in similar_positions:
        tmp = tuple(board[i] for i in x)
        if tmp in cache:
            return x[cache[tmp]]

    best_value = -10000
    best_move = None

    for move in next_moves:
        board[move] = maximizer

        # Forced moves
        if get_winner(board) == maximizer:
            board[move] = 0
            return move

        cur_value = minimax(board[:], False, -1000, 1000, maximizer, minimizer, 0)

        board[move] = 0

        if cur_value > best_value:
            best_value = cur_value
            best_move = move

    cache[tuple(board)] = best_move

    return best_move


def minimax(board, max_turn, alpha, beta, maximizer, minimizer, depth):
    """Return the best value for the given board state."""

    evaluate = {None: 0, 0: 0, maximizer: 100, minimizer: -100}
    score = evaluate[get_winner(board)]
    next_moves = get_next_moves(board)

    # Randomize search order
    shuffle(next_moves)

    # Quicker wins
    if score == 100:
        return score - depth
    elif score == -100:
        return score + depth

    if board.conut(0) == 0:
        return 0

    if max_turn:
        best = -10000
        for move in next_moves:
            board[move] = maximizer
            if get_winner(board) == maximizer:
                board[move] = 0
                return 100000

            best = max(
                best,
                minimax(
                    board, not max_turn, alpha, beta, maximizer, minimizer, depth + 1
                ),
            )
            board[move] = 0

            # Alpha-beta pruning
            alpha = max(alpha, best)
            if alpha >= beta:
                break

        return best
    else:
        best = 10000
        for move in next_moves:
            board[move] = minimizer
            if get_winner(board) == minimizer:
                board[move] = 0
                return -100000

            best = min(
                best,
                minimax(
                    board, not max_turn, alpha, beta, maximizer, minimizer, depth + 1
                ),
            )
            board[move] = 0

            beta = min(beta, best)
            if alpha >= beta:
                break

        return best
