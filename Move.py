class Move(object):
    """docstring for Move"""

    def __init__(self, row, col, to=None):
        super(Move, self).__init__()
        self.fromm = (row, col)  # Initial position
        self.to = to  # Destination
        self.eaten = []  # Pieces that were eaten in this move
        self.eats = False  # if this move eats pieces
