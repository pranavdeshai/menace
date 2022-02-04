from helper import get_next_positions, get_winner, get_best_position
from random import choices
import matplotlib.pyplot as plt


def simulate(n=1, d=0):
    """`n`: Number of games to simulate. Default is 1.

    `d`: Depth limit for minimax search. Default is 0 (random).
        -1 for no limit,
        -2 to simulate against MENACE and 
        -3 to play against human.
    """

    scoreboard = [0, 0, 0]  # Draws, wins and losses (wrt MENACE)
    changes = []
    cache = {}
    menace = {}
    if d == -2:
        menace2 = {}

    for i in range(n):
        board = [0 for i in range(9)]
        menace_moves = []
        if d == -2:
            menace2_moves = []

        game_over = False
        while not game_over:
            for player in [1, 2]:
                winner = get_winner(board)
                if winner is None:
                    next_positions = get_next_positions(board)

                    if player == 1:
                        # Add new board states to MENACE
                        state = ''.join(str(i) for i in board)
                        if state not in menace:
                            menace[state] = {}
                            for pos in next_positions:
                                menace[state][pos] = 1

                        # Get a move from MENACE
                        p = [i for i in menace[state].keys()]
                        w = [i for i in menace[state].values()]
                        position = choices(p, w)[0]

                        # Store the played moves
                        menace_moves.append((state, position))
                    else:
                        if d == -2:
                            # Add new board states to MENACE-2
                            state = ''.join(str(i) for i in board)
                            if state not in menace2:
                                menace2[state] = {}
                                for next_position in next_positions:
                                    menace2[state][next_position] = 1

                            p = [i for i in menace2[state].keys()]
                            w = [i for i in menace2[state].values()]
                            position = choices(p, w)[0]

                            menace2_moves.append((state, position))
                        elif d == -3:
                            print(f'{board[:3]}\n{board[3:6]}\n{board[6:]}\n')

                            # Get input from user
                            position = int(input('Move: '))

                            # Validate input
                            while position not in next_positions:
                                position = int(
                                    input('Invalid move. Try again: '))

                        else:
                            # Play the best move
                            position = get_best_position(board, 2, 1, cache, d)

                    board[position] = player
                else:
                    scoreboard[winner] += 1
                    game_over = True

                    changes.append(
                        3*scoreboard[1] + scoreboard[0] - scoreboard[2])

                    # Reinforce MENACE
                    for s, i in menace_moves:
                        if winner == 1:
                            menace[s][i] += 3  # Reward if won
                        elif winner == 2:
                            if menace[s][i] > 1:
                                menace[s][i] -= 1  # Punish if lost
                        else:
                            menace[s][i] += 1

                    if d == -2:
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


opponents = {
    0: 'Random',
    1: 'Depth 1',
    5: 'Depth 5',
    -1: 'Perfect',
    -2: 'MENACE',
}

for x in opponents:
    changes = simulate(100, x)
    plt.plot(changes)

plt.xlabel('Number of games')
plt.ylabel('Change in number of beads in first box')
plt.legend([opponents[x] for x in opponents], loc='upper left')
plt.show()
