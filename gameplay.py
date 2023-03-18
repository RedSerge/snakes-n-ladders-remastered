from board import *


# A class for one player, storing its name, accumulated reserve turns, dice and pieces,
# as well as a "logic" function representing the player's decisions
class Player:

    def __init__(self, name, pieces_count, logic):
        self.name = name
        self.reserve = 0
        self.dices = []
        self.pieces = [Piece() for n in range(pieces_count)]
        self.logic = logic

    # Roll the dice! If the result is FIRST_DOUBLE_DICE or higher, roll again!
    # Return all the rolling results
    @staticmethod
    def roll_dices():
        throw = []
        while True:
            dice = cube()
            throw.append(dice)
            if dice < FIRST_DOUBLE_DICE:
                break
        return throw

    # If dice can be preserved and such decision has been made by the player, do it!
    def preserve_dices(self, throw):
        can_preserve = self.reserve > 0
        if can_preserve:
            self.dices.extend(throw)
            self.reserve -= 1
        return can_preserve

    # When the player decides to move piece #piece_index across the board,
    # do it based on the rolled dice, returning the move results along the way
    def apply_dices(self, piece_index, dices):
        piece = self.pieces[piece_index]
        victory = piece.step(dices)
        gather_reserve, gather_chain = piece.results()
        self.reserve += gather_reserve
        return victory, gather_reserve, gather_chain

    # The player that didn't make it in time (or just skipped the move),
    # is forced to step back with one of his pieces on the nearest cell w/o snakes or ladders.
    # The "in-time" concept is not implemented in this version of the game, though,
    # but this function now is used to prevent bots from moving in certain modes.
    def step_back(self):
        piece = rnd.choice(self.pieces)
        while True:
            piece.pos -= 1
            if piece.pos < 0:
                piece.pos = 0
            if piece.pos not in FORCES:
                break

    # The whole routine of the game (with debug messages for the server):
    def routine(self, throw=None):
        print(f"Player {self.name} is playing (reserve: {self.reserve})\n")
        [print(f"Piece #{i + 1} is at position {j.pos}") for i, j in enumerate(self.pieces)]
        if throw is None:
            throw = self.roll_dices()
        print()
        print(f"Dice thrown: {throw}")
        sum_dices = sum(self.dices)
        if self.dices:
            print(f"Dice reserved: {self.dices}")
            print(f"Total reserved sum: {sum_dices}")
        print()

        piece_index, ask_reserve = self.logic(self, None, throw)

        if piece_index is None:
            self.step_back()
            print()
            print("!!! OUT OF TIME !!!")
            [print(f"Piece #{i + 1} is at position {j.pos}") for i, j in enumerate(self.pieces)]
            print()
            return False

        if piece_index >= 0:

            print(f"Piece #{piece_index + 1} moves")

            if sum_dices:
                if ask_reserve is None:
                    ask_reserve = self.logic(self, piece_index)
                if ask_reserve == 1:
                    print("Dice-by-dice reserve applied")
                    throw.extend(self.dices)
                    self.dices = []
                elif ask_reserve == 2:
                    print("Full reserve applied")
                    throw.append(sum_dices)
                    self.dices = []

            victory, gather_reserve, gather_chain = self.apply_dices(piece_index, throw)
            if gather_reserve:
                print(f"The reserve capacity has been increased by {gather_reserve},")
                print(f"the reserve capacity now is {self.reserve}\n")
            print(" --> ".join([str(i) for i in gather_chain]))
            if victory:
                print(f"\nPlayer {self.name} have won!")
            print()
            return victory
        else:
            can_preserve = self.preserve_dices(throw)
            if not can_preserve:
                print("You have not enough reserve capacity for this operation\n")
            else:
                print(f"Reserve applied, dice reserved: {self.dices}\n")
                return False
