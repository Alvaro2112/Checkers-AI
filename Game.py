from Board import Board
from GUI_and_Minimax import play_game

player = -1  # Who you will be, either black(-1) or white(1)                                           ###
depth = 5  # The depth of the AI in Humane vs AI mode, beware of your computers limitations     ###
bot_vs_bot = True  # AI vs AI mode                                                              ###
depth_white_bot = 6  # In case of AI vs AI sets the depth of each AI                            ###
depth_black_bot = 4  # In case of AI vs AI sets the depth of each AI                            ###

if __name__ == '__main__':
    # Create new Board
    board = Board()

    # Adds pieces to the Board
    board.add_pieces()

    # Start the Game
    play_game(board, player, depth, bot_vs_bot, depth_white_bot, depth_black_bot)
