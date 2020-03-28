from Board import Board

board = Board()
board.add_pieces()
print(board.black_pieces[1].row,board.black_pieces[1].col)
board.black_pieces[1].move_to(3,1)

