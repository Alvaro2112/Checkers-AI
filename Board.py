from Piece import Piece
class Board(object):
	"""docstring for Board"""
	


	def __init__(self):
		super(Board, self).__init__()

		BLANK = 0               # piece names
		PAWNB = -1
		PAWNW = 1
		KINGB = -2
		KINGW = 2
		self.white_pieces = []
		self.black_pieces = []
		self.board =[[0,-1]*4,
                	[BLANK,BLANK]*4,
                	[BLANK,-1]*4,
                	[0,0,0,0,1,0,0,0],
                	[BLANK,]*8,
                	[BLANK,BLANK]*4,
                	[BLANK,BLANK]*4,
                 	[BLANK,BLANK]*4]



	def board_score(self):
		score = 0
		for i in self.board:
			for j in i:
				score += j

		return score

	def move_piece(self, piece, row, col):
		
		self.board[piece.row][piece.col] = 0
		piece.row = row
		piece.col = col
		self.board[piece.row][piece.col] = piece.team
		Piece.board = self
		#for i in self.white_pieces:
		#	i.update_legal_moves()
		#for i in self.black_pieces:
		#	i.update_legal_moves()


	def print_board(self):
		for i in self.board:
			print(i)

	def add_pieces(self):
		row = 0

		for i in self.board:
			col = 0

			for j in i:

				if j == +1:
					piece = Piece(row,col,+1)
					piece.add_initial_moves()
					self.white_pieces.append(piece)

				if j == -1:
					piece = Piece(row,col,-1)
					piece.add_initial_moves()
					self.black_pieces.append(piece)

				col += 1


			row += 1


	def get_piece(self, row, col, team):
		
		if team == 1:
			for i in self.white_pieces:
				if i.row == row and i.col == col:
					return i

		else:
			for i in self.black_pieces:
				if i.row == row and i.col == col:
					return i
