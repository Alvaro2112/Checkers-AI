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
		self.score = 0
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
		score = 0
		no = 0
		for i in range(8):
			for j in range(8):
				if self.board[i][j] == 2:

					score += 5 + 8 + 2
				elif self.board[i][j] == -2:
					score -= 5 + 8 + 2
				elif self.board[i][j] == 1:
					score += 5 + (7 - i)
				elif self.board[i][j] == -1:
					score -= 5 + i 
				if self.board[i][j] != 0:
					no+=1

		self.score = score/no

		if self.draw:
			self.score = 0.0000000001
		if self.gameover and self.winner == 1:
			self.score = 999999
		if self.gameover and self.winner == -1:
			self.score = -999999


	def move_piece(self, piece, row, col):
		
		self.board[piece.row][piece.col] = 0
		piece.row = row
		piece.col = col
		self.board[piece.row][piece.col] = piece.team
		if piece.is_queen: 
			print("Changed king value")
			self.board[piece.row][piece.col] = piece.team * 2
			print(self.board[piece.row][piece.col])

		Piece.board = self

		self.tot_black_moves = []
		self.tot_white_moves = []
		
		if piece.team == -1:
			eats = False
			for i in self.white_pieces:
				i.update_legal_moves()
				eats = eats or i.can_eat
			if eats:
				for i in self.white_pieces:
					if not i.can_eat:
						i.legal_moves = []


		else:
			eats = False
			for i in self.black_pieces:
				i.update_legal_moves()
				eats = eats or i.can_eat
			if eats:
				for i in self.black_pieces:
					if not i.can_eat:
						i.legal_moves = []

		if self.won(1):
			self.gameover = True
			self.winner = 1

		if self.won(-1):
			self.gameover = True
			self.winner = -1

		if False:
			self.gameover = True
			



		self.board_score()


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


	def get_piece(self, row, col):
		
		
			for i in self.white_pieces:

				if i.row == row and i.col == col:
					return i

			for i in self.black_pieces:
				if i.row == row and i.col == col:
					return i


	def won(self, team):
		if team == 1:
			if len(self.black_pieces) == 0:
				return True
			state = True
			for i in self.black_pieces:
				if len(i.legal_moves) != 0:
					state = False
					break
			return state
		else:
			if len(self.white_pieces) == 0:
				return True
			state = True
			for i in self.white_pieces:
				if len(i.legal_moves) != 0:
					state = False
					break
			return state

	def draw(self):

		state = True
		for i in self.white_pieces:
				if len(i.legal_moves) != 0:
					state = False
					break
		for i in self.black_pieces:
				if state == False: break
				if len(i.legal_moves) != 0:
					state = False
					break
		return state


	def get_move(self, moves, row, col):
		for i in moves:
			if i.to[0] == row and i.to[1] == col:
				return i
		return None