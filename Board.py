import copy

from Move import Move
from Piece import Piece


def find_move(moves, row, col):
    """finds a move from a list of moves"""

    for i in moves:
        if i.to[0] == row and i.to[1] == col:
            return i

    return None


def out_of_board(row, col):
    if row >= 8 or col >= 8 or row < 0 or col < 0:
        return True
    return False


class Board(object):
    """docstring for Board"""

    def __init__(self):
        super(Board, self).__init__()

        # piece names
        BLANK = 0
        PAWNB = -1
        PAWNW = 1
        KINGB = -2
        KINGW = 2
        score = 0

        self.BLANK = BLANK
        self.PAWNB = PAWNB
        self.PAWNW = PAWNW
        self.KINGB = KINGB
        self.KINGW = KINGW
        self.score = score
        self.white_pieces, self.black_pieces = [], []
        self.gameover, self.draw = False, False
        self.winner = 0

        # Initial Board layout
        self.board_layout = [[BLANK, PAWNB] * 4,
                             [PAWNB, BLANK] * 4,
                             [BLANK, PAWNB] * 4,
                             [BLANK, ] * 8,
                             [BLANK, ] * 8,
                             [PAWNW, BLANK] * 4,
                             [BLANK, PAWNW] * 4,
                             [PAWNW, BLANK] * 4]

    def board_score(self):
        """This functions compute the score of the current board from blacks perspective"""

        score = 0
        no = 0  # number of pieces on board

        # Reward function can bea changed here to change each piece value
        for i in range(8):
            for j in range(8):

                if self.board_layout[i][j] == self.KINGW:
                    score -= 5 + 8 + 2 - (4 - i) if i < 4 else 5 + 8 + 2
                    score += abs(j - 4)
                    no += 1
                elif self.board_layout[i][j] == self.KINGB:
                    no += 1
                    score += 5 + 8 + 2 - (i - 5) if i > 5 else 5 + 8 + 2
                    score -= abs(j - 4)

                elif self.board_layout[i][j] == self.PAWNW:
                    no += 1
                    score -= 5 + (7 - i)
                elif self.board_layout[i][j] == self.PAWNB:
                    score += 5 + i
                    no += 1

        self.score = score / no

        if self.draw and self.winner == self.PAWNB:
            self.score = -0.0000000001

        if self.draw and self.winner == self.PAWNW:
            self.score = 0.0000000001

        if self.gameover and self.winner == self.PAWNW:
            self.score = -1000

        if self.gameover and self.winner == self.PAWNB:
            self.score = 1000

    def move_piece(self, piece, row, col):
        """this function moves a piece to a specific position"""

        # moves the piece
        self.board_layout[piece.row][piece.col] = self.BLANK
        piece.row = row
        piece.col = col
        self.board_layout[piece.row][piece.col] = piece.team

        if piece.is_queen:
            self.board_layout[piece.row][piece.col] = piece.team * 2

        pieces = self.white_pieces if piece.team == self.PAWNB else self.black_pieces

        # updates moves for other pieces and check if a piece can eat another one, if it can all other moves that do not involve eating are removed
        eats = False
        for i in pieces:
            self.update_legal_moves(i)
            eats = eats or i.can_eat
        if eats:
            for i in pieces:
                if not i.can_eat:
                    i.legal_moves = []

        if self.won(self.PAWNW):
            self.gameover = True
            self.winner = self.PAWNW

        if self.won(self.PAWNB):
            self.gameover = True
            self.winner = self.PAWNB

        if self.draww():
            self.gameover = True
            self.winner = 0

        self.board_score()

    def add_pieces(self):
        """this function add initial pieces to the board"""

        for row, i in enumerate(self.board_layout):
            for col, j in enumerate(i):

                if j == self.PAWNW:
                    piece = Piece(row, col, +1)
                    self.add_initial_moves(piece)

                    self.white_pieces.append(piece)

                if j == self.PAWNB:
                    piece = Piece(row, col, -1)
                    self.add_initial_moves(piece)
                    self.black_pieces.append(piece)

    def get_piece(self, row, col):
        """returns the piece at a specific position"""

        for i in self.white_pieces:
            if i.row == row and i.col == col:
                return i

        for i in self.black_pieces:
            if i.row == row and i.col == col:
                return i

    def won(self, team):
        pieces = self.white_pieces if team == self.PAWNB else self.black_pieces

        if len(pieces) == 0:
            return True

        for i in pieces:
            if len(i.legal_moves) != 0:
                return False

        return True

    def draww(self):
        for i in self.white_pieces:
            if len(i.legal_moves) != 0:
                return False

        for i in self.black_pieces:
            if len(i.legal_moves) != 0:
                return False

        return True

    def move_to(self, piece, row, col):
        if not self.check_pos(row, col):
            raise ValueError((row, col), "Wrong new position")

        self.becomes_king(piece, row, col)
        self.move_piece(piece, row, col)

    def update_legal_moves(self, piece):
        piece.can_eat = False
        piece.legal_moves = []
        piece.legal_moves = self.get_move(piece, piece.row, piece.col, False, Move(piece.row, piece.col))

    def get_move(self, piece, row, col, has_eaten, move):
        """updates moves"""

        moves = []

        for j in range(3):
            if j == 1: continue
            if self.is_enemmy(piece, row - piece.team, col + (j - 1) * piece.team) and self.check_pos(
                    row - 2 * piece.team,
                    col + (
                            j - 1) * 2 * piece.team) and move.eaten.count(
                (row - piece.team, col + (j - 1) * piece.team)) == 0:

                move_copy = copy.deepcopy(move)
                move_copy.to = (row - 2 * piece.team, col + (j - 1) * 2 * piece.team)
                move_copy.eaten += [(row - piece.team, col + (j - 1) * piece.team)]
                piece.can_eat = True

                result = self.get_move(piece, row - 2 * piece.team, col + (j - 1) * 2 * piece.team, True, move_copy)
                if not result:
                    result = [move_copy]
                moves += result

            if piece.is_queen and self.is_enemmy(piece, row + piece.team,
                                                 col + (j - 1) * piece.team) and self.check_pos(
                row + 2 * piece.team, col + (j - 1) * 2 * piece.team) and move.eaten.count(
                (row + piece.team, col + (j - 1) * piece.team)) == 0:

                move_copy = copy.deepcopy(move)
                move_copy.to = (row + 2 * piece.team, col + (j - 1) * 2 * piece.team)
                move_copy.eaten += [(row + piece.team, col + (j - 1) * piece.team)]
                piece.can_eat = True

                result = self.get_move(piece, row + 2 * piece.team, col + (j - 1) * 2 * piece.team, True, move_copy)
                if not result:
                    result = [move_copy]
                moves += result

        for j in range(3):
            if j == 1: continue
            if self.check_pos(row - piece.team, col + (j - 1) * piece.team) and not has_eaten and not piece.can_eat:
                move_copy = copy.deepcopy(move)
                move_copy.to = (row - piece.team, col + (j - 1) * piece.team)
                moves += [move_copy]
            if piece.is_queen and self.check_pos(row + piece.team,
                                                 col + (j - 1) * piece.team) and not has_eaten and not piece.can_eat:
                move_copy = copy.deepcopy(move)
                move_copy.to = (row + piece.team, col + (j - 1) * piece.team)
                moves += [move_copy]

        return moves

    def check_pos(self, row, col):
        if out_of_board(row, col):
            return False

        if self.board_layout[row][col] != 0:
            return False

        return True

    def is_enemmy(self, piece, row, col):
        if out_of_board(row, col):
            return False

        if self.board_layout[row][col] != -piece.team and self.board_layout[row][col] != - 2 * piece.team:
            return False
        return True

    def add_initial_moves(self, piece):
        # disable this block if you change initial board layout
        if self.check_pos(piece.row - piece.team, piece.col - piece.team):
            piece.legal_moves += [Move(piece.row, piece.col, to=(piece.row - piece.team, piece.col - piece.team))]
        if self.check_pos(piece.row - piece.team, piece.col + piece.team):
            piece.legal_moves += [Move(piece.row, piece.col, to=(piece.row - piece.team, piece.col + piece.team))]

        # enable this block if you change initial board layout
        '''
        self.update_legal_moves(piece)
        '''

    def becomes_king(self, piece, row, col):
        if piece.team == self.PAWNW and row == 0:
            piece.is_queen = True

        if piece.team == self.PAWNB and row == 7:
            piece.is_queen = True
