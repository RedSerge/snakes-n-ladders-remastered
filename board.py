import random as rnd

# Map of snakes & ladders: N: M -> from N to M
FORCES = {i: j for i, j in [
    (95, 75),
    (62, 19),
    (4, 14),
    (87, 24),
    (51, 67),
    (93, 73),
    (36, 44),
    (21, 42),
    (28, 84),
    (98, 78),
    (16, 6),
    (9, 31),
    (80, 100),
    (1, 38),
    (71, 91),
    (47, 26),
    (49, 11),
    (64, 60),
    (56, 53),
]}
LAST_PIECE = 100  # The final cell on the board
FIRST_DOUBLE_DICE = 5  # If the last dice has FIRST_DOUBLE_DICE or more, roll the dice once again


# Dice rolling
def cube():
    return rnd.randint(1, 6)


# A class for one piece, storing its position, accumulated reserve turns and steps (as a chain)
class Piece:
    def __init__(self):
        self.pos = 0  # 0 == Not on a board yet
        self.reserve = 0
        self.chain = []

    # Check if the last step was on the snake/ladder;
    # that means we are forced to deviate from the straight path to the finish
    def deviate(self):
        last_step = self.chain[-1]
        deviated = last_step in FORCES
        if deviated:
            self.chain.append(FORCES[last_step])
            # Snake gives one more chance to reserve the dice
            if FORCES[last_step] < last_step:
                self.reserve += 1
        return deviated

    # Manage the piece step ("dices" form is more convenient in this case, IMHO :) )
    # Return whether the victory occurs (the piece is on the last cell of the board) or not
    def step(self, dices):
        # Accumulated chain starts with current position, no reserve yet
        self.chain = [self.pos]
        self.reserve = 0
        for dice in dices:
            # Move according to the dice number
            new_pos = self.pos + dice
            # Overboard! Get back (remainder-based)
            if new_pos > LAST_PIECE:
                new_pos = LAST_PIECE - (new_pos % LAST_PIECE)
            # Add new position to the chain
            self.chain.append(new_pos)
            # Snake? Ladder? Combo? Anyway, unpack and wait
            while self.deviate():
                pass
            # Update current position (the last in the chain)
            self.pos = self.chain[-1]
            # Victory!
            if self.pos == LAST_PIECE:
                return True
        return False

    # Return results of the dice rolling (accumulated reserve and chain)
    def results(self):
        return self.reserve, self.chain