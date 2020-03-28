
class Piece(object):
	
	board = None

	"""docstring for Piece"""
	def __init__(self, row, col, team):
		super(Piece, self).__init__()

		self.row = row
		self.col = col
		self.team = team
		self.is_queen = False
		self.legal_moves = []
		
		

	def getPosition(self):
		return self.row, self.col

	def move_to(self, row, col):
		Piece.board.move_piece(self, row, col)
		self.row = row
		self.col = col

	def update_legal_moves(self):
		self.legal_moves = []
		self.get_move(self.row, self.col, False)

	def get_move(self, row, col, has_eaten):
		if self.check_pos(row - self.team, col - self.team) and not has_eaten:
			self.legal_moves.append((row - self.team, col - self.team))

		if self.check_pos(row - self.team, col + self.team) and not has_eaten:
			self.legal_moves.append((row - self.team, col + self.team))

		if self.is_enemmy(row - self.team, col + self.team) and self.check_pos(row - 2 * self.team, col + 2 * self.team):
			self.legal_moves.append((row - 2 * self.team, col + 2 * self.team))
			self.get_move(row - 2 * self.team, col + 2 * self.team, True)

		if self.is_enemmy(row - self.team, col - self.team) and self.check_pos(row - 2 * self.team, col - 2 * self.team):
			self.legal_moves.append((row - 2 * self.team, col - 2 * self.team))
			self.get_move(row - 2 * self.team, col - 2 * self.team, True)

	def check_pos(self, row, col):
		if row >= 8 or col >= 8 or row < 0 or col < 0:
			return False

		if Piece.board.board[row][col] != 0:
			return False
		return True

	def is_enemmy(self, row, col):
		if row >= 8 or col >= 8 or row < 0 or col < 0:
			return False
		if Piece.board.board[row][col] != -self.team:
			return False
		return True

	def add_initial_moves(self):
		if self.check_pos(self.row - self.team, self.col - self.team):
			self.legal_moves.append((self.row - self.team, self.col - self.team))
		if self.check_pos(self.row - self.team, self.col + self.team):
			self.legal_moves.append((self.row - self.team, self.col + self.team))
	

