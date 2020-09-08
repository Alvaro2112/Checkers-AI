from Board import Board
from GUI_and_Minimax import play_game

if __name__ == '__main__':
    # Create new Board
    board = Board()

    # Adds pieces to the Board
    board.add_pieces()

    # Start the Game
    play_game(board)
