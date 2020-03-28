

class Piece(object):
	"""docstring for Piece"""
	def __init__(self, row, col, team, board):
		super(Piece, self).__init__()
		self.row = row
		self.col = col
		self.team = team
		self.board = board
		self.is_queen = False
		self.legal_moves = []
		self.add_initial_moves()

	def getPosition(self):
		return self.row, self.col

	def move_to(self, row, col):
		
		self.board.move_piece(self, row, col)
		self.row = row
		self.col = col

	def update_legal_moves(self):
		pass

	def get_move(self, row,col):
		pass

	def check_pos(self, row, col):
		if row >= 10 or col >= 10 or row < 0 or col < 0:
			return False
		if self.board.board[row][col] != 0:
			return False
		return True

	def add_initial_moves(self):
		if self.team == 1 :
			if self.check_pos(self.row - 1, self.col - 1):
				self.legal_moves.append((self.row - 1, self.col - 1))
			if self.check_pos(self.row - 1, self.col + 1):
				self.legal_moves.append((self.row - 1, self.col + 1))
		else:
			if self.check_pos(self.row + 1, self.col + 1):
				self.legal_moves.append((self.row + 1, self.col + 1))
			if self.check_pos(self.row + 1, self.col - 1):
				self.legal_moves.append((self.row + 1, self.col - 1))

