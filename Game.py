from Board import Board
from Piece import Piece
from Demo_Chess_Board import PlayGame
import time
import copy

board = Board()
Piece.board = board
board.add_pieces()

'''
copyr = copy.deepcopy(board)
Piece.board = copyr
print(board.board[3][0])
print(copyr.board[3][0])
copyr.black_pieces[0].move_to(3,0)
print(board.board[3][0])
print(copyr.board[3][0])
Piece.board = board
board.black_pieces[0].move_to(3,0)
print(board.board[3][0])
print(copyr.board[3][0])
'''
#time.sleep(1111111111)

PlayGame(board)

