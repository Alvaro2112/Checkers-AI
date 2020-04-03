from Piece import Piece
from Move import Move
import copy
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
		self.white_pieces = []
		self.black_pieces = []
		self.gameover = False
		self.draw = False
		self.winner = 0
		self.board =[[BLANK,PAWNB]*4,
                	[PAWNB,BLANK]*4,
                	[BLANK,PAWNB]*4,
                	[BLANK,]*8,
                	[BLANK,]*8,
                	[PAWNW,BLANK]*4,
                	[BLANK,PAWNW]*4,
                 	[PAWNW,BLANK]*4]

	def board_score(self):
		
		self.score = 0
		score = 0
		no = 0

		for i in range(8):
			for j in range(8):

				if self.board[i][j] == self.KINGW:
					score -= 5 + 8 + 2
					no += 1
				elif self.board[i][j] == self.KINGB:
					no += 1
					score += 5 + 8 + 2
				elif self.board[i][j] == self.PAWNW:
					no += 1
					score -= 5 + (7 - i)
				elif self.board[i][j] == self.PAWNB:
					score += 5 + i 
					no += 1

		self.score = copy.deepcopy(score / no)

		if self.draw and self.winner == self.PAWNB:
			self.score = -0.0000000001

		if self.draw and self.winner ==self.PAWNW:
			self.score = 0.0000000001

		if self.gameover and self.winner == self.PAWNW:
			self.score = -1000

		if self.gameover and self.winner == self.PAWNB:
			self.score = 1000


	def move_piece(self, piece, row, col):
		
		self.board[piece.row][piece.col] = self.BLANK
		piece.row = row
		piece.col = col
		self.board[piece.row][piece.col] = piece.team

		if piece.is_queen: 
			self.board[piece.row][piece.col] = piece.team * 2

		pieces =  self.white_pieces if piece.team == self.PAWNB else self.black_pieces

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

		for row,i in enumerate(self.board):
			for col,j in enumerate(i):

				if j == self.PAWNW:
					piece = Piece(row,col,+1)
					self.add_initial_moves(piece)

					self.white_pieces.append(piece)

				if j == self.PAWNB:
					piece = Piece(row,col,-1)
					self.add_initial_moves(piece)
					self.black_pieces.append(piece)

	def get_piece(self, row, col):
		
			for i in self.white_pieces:
				if i.row == row and i.col == col:
					return i

			for i in self.black_pieces:
				if i.row == row and i.col == col:
					return i


	def won(self, team):

		pieces =  self.white_pieces if team == self.PAWNB else self.black_pieces

		if len(pieces) == 0:
			return True

		for i in pieces:
			if len(i.legal_moves) != 0:
				return False

		return True

	def draww(self):


		for i in self.white_pieces:
				if len(i.legal_moves) != 0:
					return  False

		for i in self.black_pieces:
				if len(i.legal_moves) != 0:
					return  False

		return True


	def find_move(self, moves, row, col):

		for i in moves:
			if i.to[0] == row and i.to[1] == col:
				return i

		return None

	def move_to(self, piece, row, col):

		if not self.check_pos(row,col):
			raise ValueError((row,col),"Wrong new position")
		
		self.becomes_king(piece,row, col)
		self.move_piece(piece, row, col)

	def update_legal_moves(self, piece):
		
		piece.can_eat = False
		piece.legal_moves = []
		piece.legal_moves = self.get_move(piece,piece.row, piece.col, False, Move(piece.row, piece.col))

	def get_move(self, piece, row, col, has_eaten ,move):

		moves = []

		for j in range(3):
				if j==1: continue
				if self.is_enemmy(piece, row - piece.team, col + (j-1) * piece.team) and self.check_pos(row - 2 * piece.team, col + (j-1) * 2 * piece.team) and move.eaten.count((row - piece.team, col + (j-1) * piece.team)) == 0 :
				
					move_copy = copy.deepcopy(move)
					move_copy.to = (row - 2 * piece.team, col + (j-1) * 2 * piece.team)
					move_copy.eaten += [(row - piece.team, col + (j-1) * piece.team)]
					piece.can_eat = True

					result = self.get_move(piece,row - 2 * piece.team, col + (j-1) * 2 * piece.team, True, move_copy)
					if result == []:
						result = [move_copy]
					moves += result

				if piece.is_queen and self.is_enemmy(piece,row + piece.team, col + (j-1) *  piece.team) and self.check_pos(row + 2 * piece.team, col + (j-1) * 2* piece.team) and move.eaten.count((row + piece.team, col + (j-1) *  piece.team)) == 0: 
			
					move_copy = copy.deepcopy(move)
					move_copy.to = (row + 2 * piece.team, col + (j-1) *2 * piece.team)
					move_copy.eaten += [(row + piece.team, col  + (j-1) *piece.team)]
					piece.can_eat = True

					result = self.get_move(piece,row + 2 * piece.team, col + (j-1) * 2 * piece.team, True, move_copy)
					if result == []:
						result = [move_copy]
					moves += result


		for j in range(3):
				if j==1: continue
				if self.check_pos(row - piece.team, col + (j-1) * piece.team) and not has_eaten and not piece.can_eat:
					move_copy = copy.deepcopy(move) 
					move_copy.to = (row - piece.team, col + (j-1) * piece.team)
					moves += [move_copy]
				if piece.is_queen and self.check_pos(row + piece.team, col + (j-1) * piece.team) and not has_eaten and not piece.can_eat:
					move_copy = copy.deepcopy(move)
					move_copy.to = (row + piece.team, col + (j-1) * piece.team)
					moves += [move_copy]
				
		return moves

	def out_of_board(self, row, col):

		if row >= 8 or col >= 8 or row < 0 or col < 0:
			return True
		return False

	def check_pos(self, row, col):

		if self.out_of_board(row, col):
			return False

		if self.board[row][col] != 0:
			return False
		
		return True

	def is_enemmy(self,piece, row, col):

		if self.out_of_board(row, col):
			return False

		if self.board[row][col] != -piece.team and self.board[row][col] != - 2 * piece.team:
			return False
		return True

	def add_initial_moves(self, piece):
		
		if self.check_pos(piece.row - piece.team, piece.col - piece.team):
			piece.legal_moves += [Move(piece.row,piece.col,to=(piece.row - piece.team, piece.col - piece.team))]
		if self.check_pos(piece.row - piece.team, piece.col + piece.team):
			piece.legal_moves += [Move(piece.row,piece.col,to=(piece.row - piece.team, piece.col + piece.team))]
		
		'''
		self.update_legal_moves(piece)
		'''

	def becomes_king(self, piece, row, col):
		
		if piece.team == self.PAWNW and row == 0:
			piece.is_queen = True
		
		if piece.team == self.PAWNB and row == 7:
			piece.is_queen = True
	

