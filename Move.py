

class Move(object):
	"""docstring for Move"""
	def __init__(self, row, col):
		super(Move, self).__init__()
		self.fromm = (row, col) 
		self.to = None
		self.eaten = []
		self.dir = 0