from Move import Move
import copy

class Piece(object):
	
	board = None

	"""docstring for Piece"""
	def __init__(self, row, col, team):
		super(Piece, self).__init__()

		self.row = row
		self.col = col
		self.team = team
		self.is_queen = True
		self.legal_moves = []
		self.can_eat = False
		self.dead = False
		

	def getPosition(self):
		return self.row, self.col

	def move_to(self, row, col):
		if not self.check_pos(row,col):
			raise ValueError((row,col),"Wrong new position")
		Piece.board.move_piece(self, row, col)
		self.row = row
		self.col = col

	def update_legal_moves(self):
		self.legal_moves = []
		self.can_eat = False
		self.get_move(self.row, self.col, False, Move(self.row, self.col))
		

	def get_move(self, row, col, has_eaten ,move):

		if self.is_enemmy(row - self.team, col + self.team) and self.check_pos(row - 2 * self.team, col + 2 * self.team) and move.eaten.count(Piece.board.get_piece(row - self.team, col + self.team, -self.team)) == 0 :
			move_copy1 = move
			if move.dir != 1:
				move_copy1 = (move)
				move_copy1.dir = 1
			move_copy1.to = (row - 2 * self.team, col + 2 * self.team)
			move_copy1.eaten.append(Piece.board.get_piece(row - self.team, col + self.team, -self.team))
			self.can_eat = True
			self.legal_moves.append(move_copy1)
			self.get_move(row - 2 * self.team, col + 2 * self.team, True, move_copy1)

		if self.is_queen and self.is_enemmy(row + self.team, col + self.team) and self.check_pos(row + 2 * self.team, col + 2 * self.team) and move.eaten.count(Piece.board.get_piece(row + self.team, col + self.team, -self.team)) == 0 :
			
			move_copy2 = move
			if move.dir != 2:
				move_copy2 = (move)
				move_copy2.dir = 2
			move_copy2.to = (row + 2 * self.team, col + 2 * self.team)			
			move_copy2.eaten.append(Piece.board.get_piece(row + self.team, col + self.team, -self.team))
			self.can_eat = True
			self.legal_moves.append(move_copy2)
			self.get_move(row + 2 * self.team, col + 2 * self.team, True, move_copy2)

		if self.is_enemmy(row - self.team, col - self.team) and self.check_pos(row - 2 * self.team, col - 2 * self.team) and move.eaten.count(Piece.board.get_piece(row - self.team, col - self.team, -self.team)) == 0 :
			move_copy3 = move
			if move.dir != 3:
				move_copy3 = (move)
				move_copy3.dir = 3
			move_copy3.to = (row - 2 * self.team, col - 2 * self.team)
			move_copy3.eaten.append(Piece.board.get_piece(row - self.team, col - self.team, -self.team))
			self.can_eat = True
			self.legal_moves.append(move_copy3)
			self.get_move(row - 2 * self.team, col - 2 * self.team, True, move_copy3)

		if self.is_queen and self.is_enemmy(row + self.team, col - self.team) and self.check_pos(row + 2 * self.team, col - 2 * self.team) and move.eaten.count(Piece.board.get_piece(row + self.team, col - self.team, -self.team)) == 0: 
			move_copy4 = move
			if move.dir != 4:
				move_copy4 = (move)
				move_copy4.dir = 4
			move_copy4.to = (row + 2 * self.team, col - 2 * self.team)
			move_copy4.eaten.append(Piece.board.get_piece(row + self.team, col - self.team ,-self.team))
			self.can_eat = True
			self.legal_moves.append(move_copy4)
			self.get_move(row + 2 * self.team, col - 2 * self.team, True, move_copy4)

		if self.check_pos(row - self.team, col - self.team) and not has_eaten and not self.can_eat:
			move_copy = copy.deepcopy(move) 
			move_copy.to = (row - self.team, col - self.team)
			self.legal_moves.append(move_copy)

		if self.check_pos(row - self.team, col + self.team) and not has_eaten and not self.can_eat:
			move_copy = copy.deepcopy(move) 
			move_copy.to = (row - self.team, col + self.team)
			self.legal_moves.append(move_copy)

		if self.is_queen and self.check_pos(row + self.team, col - self.team) and not has_eaten and not self.can_eat:
			move_copy = copy.deepcopy(move)
			move_copy.to = (row + self.team, col - self.team)
			self.legal_moves.append(move_copy)

		if self.is_queen and self.check_pos(row + self.team, col + self.team) and not has_eaten and not self.can_eat:
			move_copy = copy.deepcopy(move)
			move_copy.to = (row + self.team, col + self.team)
			self.legal_moves.append(move_copy)



	def out_of_board(self, row, col):
		if row >= 8 or col >= 8 or row < 0 or col < 0:
			return True
		return False

	def check_pos(self, row, col):
		if self.out_of_board(row, col):
			return False

		if Piece.board.board[row][col] != 0:
			return False
		
		return True

	def is_enemmy(self, row, col):
		if self.out_of_board(row, col):
			return False
		if Piece.board.board[row][col] != -self.team:
			return False
		return True

	def add_initial_moves(self):
		if self.check_pos(self.row - self.team, self.col - self.team):
			self.legal_moves.append((self.row - self.team, self.col - self.team))
		if self.check_pos(self.row - self.team, self.col + self.team):
			self.legal_moves.append((self.row - self.team, self.col + self.team))
	

