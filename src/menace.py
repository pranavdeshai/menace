from helper import get_next_moves, get_best_move, get_winner
from random import choices
from sys import argv


def simulate(m=0, n=100):
    """Simulate games and return the results.

    `m`: Mode of gameplay. Default is 0 (random).
        [-1, 0, ...] sets depth limit for minimax search. -1 for no limit.
        -2 to simulate against MENACE and 
        -3 to play against human.
    `n`: Number of games to simulate. Default is 100.
    """

    scoreboard = [0, 0, 0]  # Draws, wins and losses (wrt MENACE)
    changes = []
    cache = {}
    menace = {}

    if m == -2:
        menace2 = {}

    players = [1, 2]
    for i in range(n):
        board = [0 for _ in range(9)]
        menace_moves = set()
        if m == -2:
            menace2_moves = set()

        game_over = False
        while not game_over:
            for player in players:
                winner = get_winner(board)
                if winner is None:
                    next_moves = get_next_moves(board)

                    if player == 1:
                        # Add new board states to MENACE
                        state = tuple(board)
                        if state not in menace:
                            menace[state] = {}
                            for move in next_moves:
                                menace[state][move] = 1

                        # Get a move from MENACE
                        p = [_ for _ in menace[state].keys()]
                        w = [_ for _ in menace[state].values()]
                        move = choices(p, w)[0]

                        # Store the played moves
                        menace_moves.add((state, move))
                    else:
                        if m == -2:
                            # Add new board states to MENACE-2
                            state = tuple(board)
                            if state not in menace2:
                                menace2[state] = {}
                                for move in next_moves:
                                    menace2[state][move] = 1

                            p = [_ for _ in menace2[state].keys()]
                            w = [_ for _ in menace2[state].values()]
                            move = choices(p, w)[0]

                            menace2_moves.add((state, move))
                        elif m == -3:
                            print(f'{board[:3]}\n{board[3:6]}\n{board[6:]}\n')

                            # Get input from user
                            move = int(input('Move: '))

                            # Validate input
                            while move not in next_moves:
                                move = int(
                                    input(f'Invalid move. Choose from the below\n{next_moves}: '))

                        else:
                            # Play the best move
                            move = get_best_move(
                                board, next_moves, 2, 1, cache, m)

                    board[move] = player
                else:
                    scoreboard[winner] += 1
                    game_over = True

                    changes.append(
                        3*scoreboard[1] + scoreboard[0] - scoreboard[2])

                    # Reinforce MENACE
                    for s, i in menace_moves:
                        if winner == 1:
                            menace[s][i] += 3
                        elif winner == 2:
                            if menace[s][i] > 1:
                                menace[s][i] -= 1
                        else:
                            menace[s][i] += 1

                    if m == -2:
                        for s, i in menace2_moves:
                            if winner == 2:
                                menace2[s][i] += 3
                            elif winner == 1:
                                if menace2[s][i] > 1:
                                    menace2[s][i] -= 1
                            else:
                                menace2[s][i] += 1
                    break
    print(scoreboard)
    return changes


params = []
for arg in argv[1:]:
    try:
        params.append(int(arg))
    except:
        print(f'Ignoring invalid argument: {arg}')

simulate(*params)
