import random as rnd
from board import Piece

# A bunch of default logic templates (as functions);

# 1st argument - the player class ("self")
# 2nd argument - the piece to move
# 3rd argument - the dice rolling result

# The first logic request is propagated w/o 2nd argument (None),
# asking for the index of the piece to be moved, and the type of
# reserve spending approach to be returned:
# (None - ask me later with the second logic request,
# 0 - none, 1 - dice-by-dice, 2 - full)
# Note: if the index of the piece is negative,
# the gameplay routine tries to reserve the dice result,
# if available/possible. It's up to the logic function to
# check if this operation is available/possible.


# The second logic request is propagated with the 2nd argument,
# but without the third one, asking strictly for the type of
# reserve spending approach to be returned:
# (0 - none, 1 - dice-by-dice, 2 - full)

# The second request is used for the text-based implementation of the game,
# when the human player uses keyboard to provide a two-stage answer.
# For bots and in cases when the answer can be provided immediately it is
# recommended to use the one-stage approach with the first logic request only.


def human_logic(player, piece, throw):
    if piece is None:
        while True:
            x = None
            while not x:
                y = input("Piece index to move (0 - to preserve, N* - ask reserve): ")
                ask_reserve = '*' in y
                x = ''.join([i for i in y if i.isdigit()])
            piece_index = int(x) - 1
            return piece_index, (None if ask_reserve else 0)
    else:
        x = input(f"Do you want to apply reserve? (0 - no, 1 - dice-by-dice, 2 - full) ")
        try:
            x = int(x)
        except:
            x = 0
        return x


def classic_logic(player, piece, throw): return 0, 0


def random_logic(player, piece, throw): return rnd.randint(-1, 1), rnd.randint(0, 2)


def bot_logic(player, piece, throw):
    piece_check = Piece()

    piece_score = []

    for i, j in enumerate(player.pieces):
        throws = throw[:], throw[:], throw[:]
        throws[1].extend(player.dices)
        throws[2].append(sum(player.dices))

        diff = []

        for v, t in enumerate(throws):
            piece_check.pos = j.pos
            if piece_check.step(t):
                return i, v

            g_reserve, g_chain = piece_check.results()
            score = (g_chain[-1] - j.pos) + (0.001 * g_reserve)
            diff.append((v, score))

        piece_score.append((i, sorted(diff, key=lambda x: -x[1])[0]))

    positive_score = [i for i in piece_score if i[1][1] > 0]
    if player.reserve and not positive_score:
        return -1, None

    piece_score = sorted(piece_score, key=lambda x: -x[1][1])

    return piece_score[0][0], piece_score[0][1][0]


def defeated_logic(player, piece, throw):
    return None, None


def server_logic(state):

    def logic_sample(player, piece, throw):
        return state[4], state[5]

    return logic_sample
