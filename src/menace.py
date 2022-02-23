from random import choice, choices
from sys import argv

from helper import get_best_move, get_next_moves, get_winner

if "-g" in argv:
    import matplotlib.pyplot as plt


def simulate(mode="-r", trials=100, graph=False):
    """Simulate games against MENACE.

    mode (str): Opponent mode. Defaults to '-r' (random).
        -r: random
        -p: perfect
        -m: MENACE-2
        -h: human
    trials (int): Number of games to simulate. Defaults to 100.
    graph (bool): Plot graph of changes. Defaults to False (no graph).
    """

    scoreboard = [0, 0, 0]  # Draws, wins and losses (wrt MENACE)
    changes = []
    menace = {}

    if mode == "-m":
        menace2 = {}

    players = [1, 2]
    for i in range(trials):
        board = [0 for _ in range(9)]
        menace_moves = set()
        if mode == "-m":
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
                        if mode == "-r":
                            move = choice(next_moves)
                        elif mode == "-p":
                            move = get_best_move(board, next_moves, 2, 1)
                        elif mode == "-m":
                            state = tuple(board)
                            if state not in menace2:
                                menace2[state] = {}
                                for move in next_moves:
                                    menace2[state][move] = 1

                            p = [_ for _ in menace2[state].keys()]
                            w = [_ for _ in menace2[state].values()]
                            move = choices(p, w)[0]

                            menace2_moves.add((state, move))
                        elif mode == "-h":
                            print(f"{board[:3]}\n{board[3:6]}\n{board[6:]}\n")

                            move = int(input("Move: "))
                            while move not in next_moves:
                                move = int(
                                    input(
                                        f"Invalid move. Choose from the below\n{next_moves}: "
                                    )
                                )

                    board[move] = player
                else:
                    scoreboard[winner] += 1
                    game_over = True

                    changes.append(3 * scoreboard[1] + scoreboard[0] - scoreboard[2])

                    # Reinforce MENACE
                    for s, i in menace_moves:
                        if winner == 1:
                            menace[s][i] += 3
                        elif winner == 2:
                            if menace[s][i] > 1:
                                menace[s][i] -= 1
                        else:
                            menace[s][i] += 1

                    if mode == "-m":
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

    if graph:
        plt.title(modes[mode])
        plt.plot(changes)
        plt.show()

    return


# Command Line Interface: "python3 menace.py [mode] [trials] [graph]"
modes = {"-r": "Random", "-p": "Perfect", "-m": "MENACE-2", "-h": "Human"}
kwargs = {}
for arg in argv[1:]:
    if arg in modes:
        kwargs["mode"] = arg
    elif arg.isnumeric():
        kwargs["trials"] = int(arg)
    elif arg == "-g":
        kwargs["graph"] = True
    else:
        print(f'Ignoring illegal argument: "{arg}"')

simulate(**kwargs)
