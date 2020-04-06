

class Move(object):
	"""docstring for Move"""
	def __init__(self, row, col,to = None):
		super(Move, self).__init__()
		self.fromm = (row, col) 
		self.to = to
		self.eaten = [] #Pieces that were eaten in this move
		self.eats = False # if this move eats pieces
