from Piece import Piece
class Board(object):
	"""docstring for Board"""
	def __init__(self):
		super(Board, self).__init__()
		self.white_pieces = []
		self.black_pieces = []
		self.board =   [[0,-1,0,-1,0,-1,0,-1,0,-1],
						[-1,0,-1,0,-1,0,-1,0,-1,0],
						[0,-1,0,-1,0,-1,0,-1,0,-1],
						[-1,0,-1,0,-1,0,-1,0,-1,0],
						[0,0,0,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0],
						[0,1,0,1,0,1,0,1,0,1],
						[1,0,1,0,1,0,1,0,1,0],
						[0,1,0,1,0,1,0,1,0,1],
						[1,0,1,0,1,0,1,0,1,0],]

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


	def print_board(self):
		for i in self.board:
			print(i)

	def add_pieces(self):
		row = 0

		for i in self.board:
			col = 0

			for j in i:

				if j == 1:
					self.white_pieces.append(Piece(row,col,1,self))
				if j == -1:
					self.black_pieces.append(Piece(row,col,-1,self))

				col += 1


			row += 1