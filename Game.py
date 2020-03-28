from Board import Board

board = Board()
board.add_pieces()
for i in range(20):
    print(board.white_pieces[i].legal_moves)
