from Board import Board
from GUI_and_Minimax import PlayGame

if __name__ == '__main__':
    # Create new Board
    board = Board()

    # Adds pieces to the Board
    board.add_pieces()

    # Start the Game
    PlayGame(board)
