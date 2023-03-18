from flask import Flask, render_template, jsonify, request
from datetime import datetime
from os.path import exists
import gameplay
from board import LAST_PIECE
from logic_templates import bot_logic, defeated_logic, server_logic

# Sorry everyone who reads this, I had no time nor wish to properly format and implement
# the whole frontend/backend wrapping around the logic of the game, it is a hastily-written
# concept demo that I wanted to share with my non-Bash/PowerShell friends who needs UI
# to understand what's going on :) . Therefore, it's strictly localhost, no multi-anything,
# no login, no nothing. Enough to play; enough to blame.

# The point is: please, do NOT use in production/hosting - for your own good :) .

app = Flask(__name__)
state = []
shadow = []

linked_logic = server_logic(state)


def init(force=False, listen_shadow=False):
    global state
    global shadow
    if force or not state:

        shadow_access = listen_shadow and len(shadow) >= 2 and len(shadow[0]) < 3 and shadow[0][1] is not None
        if shadow_access:
            shadow[0].append(shadow[0][1] - shadow[0][0])
            shadow[0][0] = shadow[0][1] = None
        else:
            shadow = [[None, None], []]

        if exists(".nobots"):
            shadow_access = True

        state.clear()
        state.extend([
            gameplay.Player("Player", 2, linked_logic),
            gameplay.Player("Veteran", 2, bot_logic if not shadow_access else defeated_logic),
            0,
            shadow_read(0),
            None,
            None
        ])


def shadow_reveal():
    shadow[0][1] = datetime.now()
    if len(shadow[0]) < 3:
        return
    print("=== TOURNAMENT OF THE SHADOWS RESULT: ===")

    steps_now = state[2]
    steps_opp = len(shadow[1]) - 1
    steps_won = steps_now <= steps_opp
    time_now = shadow[0][1] - shadow[0][0]
    time_opp = shadow[0][2]
    time_won = time_now <= time_opp

    result = []
    if not steps_won:
        result.append("rounds")
    if not time_won:
        result.append("time")
    if result:
        result = ' and '.join(result)
        result = f'DEFEAT by {result}'
    else:
        result = "VICTORY!"

    print(f"{steps_now} VS {steps_opp}")
    print(f"{time_now} VS {time_opp}")
    print(f"\nRESULT: {result}\n")
    print("=== *** ===")
    print()


def shadow_write(val):
    if len(shadow[0]) < 3:
        shadow[1].append(val)


def shadow_read(val):
    read_shadows = len(shadow[0]) >= 3 and val < len(shadow[1])
    return shadow[1][val] if read_shadows else gameplay.Player.roll_dices()


@app.route("/")
def entry_point():
    return render_template('snakes.htm')


@app.route("/step", methods=['POST'])
def step():
    init()
    req = request.get_json(force=True)
    cde = req.get('code', None)
    if cde == 'EXTERMINATUS':
        init(True)
    elif cde == 'SHADOWTOUR':
        init(True, True)
    elif LAST_PIECE not in [
        state[0].pieces[0].pos,
        state[0].pieces[1].pos,
        state[1].pieces[0].pos,
        state[1].pieces[1].pos
    ]:
        if cde:
            if len(cde) >= 2:
                accepted = False
                print(cde, state[0].reserve)
                if cde[0] == '`' and state[0].reserve:
                    state[4], state[5] = -1, None
                    accepted = True
                elif cde[0] in ['1', '2']:
                    piece = 0 if cde[0] == '1' else 1
                    mode = 0
                    if cde[1] == '[':
                        mode = 1
                    elif cde[1] == ']':
                        mode = 2
                    state[4], state[5] = piece, mode
                    accepted = True
                if accepted:

                    if not state[2]:
                        shadow_write(state[3])
                        shadow[0][0] = datetime.now()

                    state[2] += 1
                    check_vi = state[0].routine(state[3])

                    state[3] = shadow_read(state[2])
                    shadow_write(state[3][:])
                    state[1].routine()

                    print("Shadow state:", shadow)
                    print()

                    if check_vi:
                        shadow_reveal()

    return jsonify({
        "throwing": state[3],
        "cache": state[0].dices,
        "pos1": state[0].pieces[0].pos,
        "pos2": state[0].pieces[1].pos,
        "posOpp1": state[1].pieces[0].pos,
        "posOpp2": state[1].pieces[1].pos,
        "step": state[2],
        "cacheable": state[0].reserve
    })


if __name__ == '__main__':
    app.run(debug=True)
