class Piece(object):

	"""docstring for Piece"""
	def __init__(self, row, col, team):
		super(Piece, self).__init__()

		self.row = row
		self.col = col
		self.team = team
		self.is_queen = False
		self.can_eat = False
		self.legal_moves = []