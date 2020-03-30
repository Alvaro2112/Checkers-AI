

class Move(object):
	"""docstring for Move"""
	def __init__(self, row, col, piece,to = None):
		super(Move, self).__init__()
		self.fromm = (row, col) 
		self.to = to
		self.eaten = []
		self.eats = False
		self.dir = 0
		self.piece = piece