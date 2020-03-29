from Board import Board
from Piece import Piece
from Demo_Chess_Board import PlayGame
from random import randint

seen = set()


def gencoordinates(m, n):
    x, y = randint(m, n) , randint(m, n) 
    while (x, y) in seen:
    	x, y = randint(m, n), randint(m, n)

    seen.add((x, y))
    return (x,y)




board = Board()
Piece.board = board
board.add_pieces()


'''
for i in range(12):
	x = gencoordinates(0,7)
	piece = Piece(x[0],x[1],-1)
	piece.add_initial_moves()
	board.black_pieces.append(piece)
	board.board[x[0]][x[1]] = -1


for i in range(12):
	x = gencoordinates(0,7)
	piece = Piece(x[0],x[1],1)
	piece.add_initial_moves()
	board.white_pieces.append(piece)
	board.board[x[0]][x[1]] = 1
'''


board.white_pieces[0].update_legal_moves()

PlayGame(board.board, board.white_pieces[0].legal_moves, board.white_pieces[0].row, board.white_pieces[0].col)
