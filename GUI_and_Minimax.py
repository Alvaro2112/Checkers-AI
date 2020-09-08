import copy
import math
import os

import PySimpleGUI as sg

import Board
from Board import Board

button_names = ('close', 'cookbook', 'cpu', 'github', 'pysimplegui', 'run', 'storage', 'timer')

CHESS_PATH = '.'  # path to the chess pieces

BLANK = 0  # piece names
PAWNB = -1
PAWNW = 1
KINGB = -2
KINGW = 2

blank = os.path.join(CHESS_PATH, 'Images/blank.png')  # You might need to change this
pawnB = os.path.join(CHESS_PATH, 'Images/npawnb.png')
pawnW = os.path.join(CHESS_PATH, 'Images/npawnw.png')
kingB = os.path.join(CHESS_PATH, 'Images/nkingb.png')
kingW = os.path.join(CHESS_PATH, 'Images/nkingw.png')

images = {PAWNB: pawnB, PAWNW: pawnW, KINGB: kingB, KINGW: kingW, BLANK: blank}


def minimax(board, depth, team, alpha, beta):
    best_move = None
    best_move_piece = None
    best_board_layout = None

    if depth == 0 or board.gameover:
        return None, None, copy.deepcopy(board.score), copy.deepcopy(board.board_layout)

    if team == 1:
        best_score = math.inf
        pieces = board.white_pieces
    else:
        best_score = -math.inf
        pieces = board.black_pieces

    for a, i in enumerate(pieces):  # loop through pieces

        for b, j in enumerate(i.legal_moves):  # loop through legal moves of each piece

            board_save = copy.deepcopy(board)  # saves current board satate

            if team == 1:
                next_pos = board_save.white_pieces[a].legal_moves[b].to

                for x, y in j.eaten:  # removes eaten pieces from board
                    board_save.board_layout[x][y] = 0
                    board_save.black_pieces.remove(board_save.get_piece(x, y))

                board_save.move_to(board_save.white_pieces[a], next_pos[0], next_pos[1])  # move the piece on board

            else:

                next_pos = board_save.black_pieces[a].legal_moves[b].to

                for x, y in j.eaten:
                    board_save.board_layout[x][y] = 0
                    board_save.white_pieces.remove(board_save.get_piece(x, y))

                board_save.move_to(board_save.black_pieces[a], next_pos[0], next_pos[1])

            _, _, score, board_layout = minimax(board_save, depth - 1, -team, alpha, beta)  # continue recursively

            if score > best_score and team == -1:
                best_board_layout = copy.deepcopy(board_layout)
                best_score = copy.deepcopy(score)
                best_move = copy.deepcopy(j)
                best_move_piece = copy.deepcopy(i)

            if score < best_score and team == 1:
                best_board_layout = copy.deepcopy(board_layout)
                best_score = copy.deepcopy(score)
                best_move = copy.deepcopy(j)
                best_move_piece = copy.deepcopy(i)

            if team == 1 and beta > score:  # Alpha beta prunning
                beta = copy.deepcopy(score)

            if team == -1 and alpha < score:
                alpha = copy.deepcopy(score)

            if beta <= alpha:
                return best_move_piece, best_move, best_score, best_board_layout

    return best_move_piece, best_move, best_score, best_board_layout


def render_square(image, key, location):
    if (location[0] + location[1]) % 2:
        color = '#B58863'
    else:
        color = '#F0D9B5'
    return sg.RButton('', image_filename=image, size=(1, 1), button_color=('white', color), pad=(0, 0), key=key)


def redraw_board(window, board, row=10, col=10, moves=(10, 10)):
    for i in range(8):
        for j in range(8):

            color = '#B58863' if (i + j) % 2 else '#F0D9B5'
            if moves.count((i, j)) != 0:
                color = '#A58888'

            if i == row and col == j:
                color = '#B46888'

            piece_image = images[board[i][j]]
            elem = window.FindElement(key=(i, j))
            elem.Update(button_color=('white', color),
                        image_filename=piece_image, )


def check_game_state(board):
    if board.winner == 0 and board.gameover:
        print("DRAW!!")
    if board.winner == 1:
        print("White Wins!!")
    if board.winner == -1:
        print("Black Wins!!")


def bot_play(boardx, team, depth, window):
    global move, piece_from
    moves = 0
    my_pieces = boardx.black_pieces if team == -1 else boardx.white_pieces
    enemy_pieces = boardx.black_pieces if team == 1 else boardx.white_pieces
    for i in my_pieces:
        for j in i.legal_moves:
            piece_from = i
            move = j
            moves += 1

    if moves > 1:
        if team == 1:
            print("White is thinking...")
        else:
            print("Black is thinking...")

        piece_from, move, score, board_layoutt = minimax(boardx, depth, team, -1000000, 1000000)
        redraw_board(window, board_layoutt)

    piece_from = boardx.get_piece(piece_from.row, piece_from.col)
    frommm = copy.deepcopy([tuple((piece_from.row, piece_from.col))])
    to = move.to

    for x, y in move.eaten:
        boardx.board_layout[x][y] = 0
        enemy_pieces.remove(boardx.get_piece(x, y))

    boardx.move_to(piece_from, to[0], to[1])
    redraw_board(window, boardx.board_layout, to[0], to[1], frommm)
    check_game_state(boardx)


def play_game(boardx, playern, depthn, bot_vs_botn, depth_white_botn, depth_black_botn):
    global button, value
    sg.ChangeLookAndFeel('GreenTan')

    # create initial board setup
    # the main board display layout
    board_layout = [[sg.T('     ')] + [sg.T('{}'.format(a), pad=((23, 27), 0), font='Any 13') for a in 'abcdefgh']]

    # loop though board and create buttons with images
    for i in range(8):
        row = [sg.T(str(8 - i) + '   ', font='Any 13')]
        for j in range(8):
            piece_image = images[boardx.board_layout[i][j]]
            row.append(render_square(piece_image, key=(i, j), location=(i, j)))
        row.append(sg.T(str(8 - i) + '   ', font='Any 13'))
        board_layout.append(row)

    # add the labels across bottom of board
    board_layout.append([sg.T('     ')] + [sg.T('{}'.format(a), pad=((23, 27), 0), font='Any 13') for a in 'abcdefgh'])

    board_controls = [[sg.RButton('Start Game')],
                      [sg.RButton('New Game')],
                      [sg.RButton('Resign Game')],
                      [sg.CBox('Play as White', key='r', default=False, disabled=False)]]

    board_tab = [[sg.Column(board_layout)]]

    # the main window layout
    layout = [[sg.TabGroup([[sg.Tab('Board', board_tab)]], title_color='red'), sg.Column(board_controls)],
              [sg.Text(text='Press Start Game to start', font='_ 14', key='info')]]

    window = sg.Window('Checkers', default_button_element_size=(12, 1), auto_size_buttons=False,
                       icon='kingb.ico').Layout(
        layout)

    # DO NOT CHANGE THESE VARIABLES #
    black = -1
    white = 1
    whos_turn = black
    fromm = None
    piece_from = None
    started = False  # Has the game started
    closed = False  # Is window closed

    # CHANGE THESE VARIABLES IN FUNCTION OF WHAT GAME MODE YOU WANT

    player = playern  # Who you will be, either black or white                                           ###
    depth = depthn  # The depth of the AI in Humane vs AI mode, beware of your computers limitations     ###
    bot_vs_bot = bot_vs_botn  # AI vs AI mode                                                            ###
    depth_white_bot = depth_white_botn  # In case of AI vs AI sets the depth of each AI                  ###
    depth_black_bot = depth_black_botn  # In case of AI vs AI sets the depth of each AI                  ###

    while True:

        if closed:
            break

        if not started:
            button, value = window.Read() if (whos_turn == player and not bot_vs_bot) else window.Read(timeout=0)

        if button in (None, 'Exit'):
            break

        if button in (None, 'Start Game'):
            started = True
            window.FindElement('info').Update(visible=False)
            if value['r']:
                player = white
                whos_turn = white
            else:
                player = black
                whos_turn = black
            window.FindElement('r').Update(disabled=True)

        while started:

            button, value = window.Read() if (whos_turn == player and not bot_vs_bot) else window.Read(timeout=0)

            if button in (None, 'Exit'):
                closed = True
                break

            elif button in (None, 'Resign Game'):
                boardx.winner = -1
                boardx.gameover = 1
                check_game_state(boardx)

            elif button in (None, 'New Game'):
                board = Board()
                board.add_pieces()
                boardx = board
                whos_turn = black
                fromm = None
                piece_from = None
                started = False
                window.FindElement('r').Update(disabled=False)
                window.FindElement('info').Update(visible=True)
                redraw_board(window, boardx.board_layout)

            elif not boardx.gameover and (whos_turn != player or bot_vs_bot):
                depth_white_bot = depth if not bot_vs_bot else depth_white_bot
                depth = depth_black_bot if whos_turn == black and bot_vs_bot else depth_white_bot

                bot_play(boardx, whos_turn, depth, window)

                fromm = None
                piece_from = None
                whos_turn = - whos_turn

            elif type(button) == type(()) and not boardx.gameover and whos_turn == player and not bot_vs_bot:

                if (whos_turn == boardx.board_layout[button[0]][button[1]] or boardx.board_layout[button[0]][
                    button[1]] == 2 * whos_turn):
                    fromm = button
                    piece_from = boardx.get_piece(fromm[0], fromm[1])
                    redraw_board(window, boardx.board_layout, piece_from.row, piece_from.col,
                                 list(o.to for o in piece_from.legal_moves))

                if (boardx.board_layout[button[0]][button[1]] == 0) and fromm is not None:

                    move = Board.find_move(piece_from.legal_moves, button[0], button[1])

                    if move is not None:

                        to = button

                        for x, y in move.eaten:
                            boardx.board_layout[x][y] = 0
                            pieces = boardx.black_pieces if player == white else boardx.white_pieces
                            pieces.remove(boardx.get_piece(x, y))

                        boardx.move_to(piece_from, to[0], to[1])
                        redraw_board(window, boardx.board_layout)
                        check_game_state(boardx)

                        fromm = None
                        piece_from = None
                        whos_turn = - whos_turn
