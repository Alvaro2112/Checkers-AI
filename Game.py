from Board import Board
from Piece import Piece
from Demo_Chess_Board import PlayGame




board = Board()
Piece.board = board
board.add_pieces()

board.black_pieces[9].move_to(4,3)
board.black_pieces[4].move_to(3,6)
board.white_pieces[2].update_legal_moves()

PlayGame(board.board,board.white_pieces[2].legal_moves)
