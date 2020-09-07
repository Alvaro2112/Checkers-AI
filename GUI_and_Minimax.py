import copy
import os

import PySimpleGUI as sg
import chess
import chess.pgn

from Board import Board

button_names = ('close', 'cookbook', 'cpu', 'github', 'pysimplegui', 'run', 'storage', 'timer')

CHESS_PATH = '.'  # path to the chess pieces

BLANK = 0  # piece names
PAWNB = -1
PAWNW = 1
KINGB = -2
KINGW = 2

blank = os.path.join(CHESS_PATH, 'Images/blank.png')
pawnB = os.path.join(CHESS_PATH, 'Images/npawnb.png')
pawnW = os.path.join(CHESS_PATH, 'Images/npawnw.png')
kingB = os.path.join(CHESS_PATH, 'Images/nkingb.png')
kingW = os.path.join(CHESS_PATH, 'Images/nkingw.png')

images = {PAWNB: pawnB, PAWNW: pawnW, KINGB: kingB, KINGW: kingW, BLANK: blank}


def Minimax(board, depth, team, alpha, beta):
    best_move = None
    best_move_piece = None
    done = False

    if depth == 0 or board.gameover:
        return (None, None, copy.deepcopy(board.score))

    if team == 1:
        best_score = 1000000
        pieces = board.white_pieces
    else:
        best_score = -1000000
        pieces = board.black_pieces

    for a, i in enumerate(pieces):
        if done:
            break
        for b, j in enumerate(i.legal_moves):

            board_save = copy.deepcopy(board)
            if team == 1:
                next_pos = board_save.white_pieces[a].legal_moves[b].to

                for x, y in j.eaten:
                    board_save.board_layout[x][y] = 0
                    board_save.black_pieces.remove(board_save.get_piece(x, y))

                board_save.move_to(board_save.white_pieces[a], next_pos[0], next_pos[1])

            else:
                next_pos = board_save.black_pieces[a].legal_moves[b].to
                for x, y in j.eaten:
                    board_save.board_layout[x][y] = 0
                    board_save.white_pieces.remove(board_save.get_piece(x, y))

                board_save.move_to(board_save.black_pieces[a], next_pos[0], next_pos[1])

            _, _, score = Minimax(board_save, depth - 1, -team, alpha, beta)

            if score > best_score and team == -1:
                best_score = copy.deepcopy(score)
                best_move = copy.deepcopy(j)
                best_move_piece = copy.deepcopy(i)

            if score < best_score and team == 1:
                best_score = copy.deepcopy(score)
                best_move = copy.deepcopy(j)
                best_move_piece = copy.deepcopy(i)

            if team == 1 and beta > score:
                beta = copy.deepcopy(score)

            if team == -1 and alpha < score:
                alpha = copy.deepcopy(score)

            if beta <= alpha:
                return (best_move_piece, best_move, best_score)

    return (best_move_piece, best_move, best_score)


def open_pgn_file(filename):
    pgn = open(filename)
    first_game = chess.pgn.read_game(pgn)
    moves = [move for move in first_game.main_line()]

    return moves


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
    if board.winner == 0 and board.gameover == True:
        print("DRAW!!")
    if board.winner == 1:
        print("White Wins!!")
    if board.winner == -1:
        print("Black Wins!!")


def PlayGame(boardx):
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
                      [sg.CBox('Play as White', key='_white_')]]

    board_tab = [[sg.Column(board_layout)]]

    # the main window layout
    layout = [[sg.TabGroup([[sg.Tab('Board', board_tab)]], title_color='red'), sg.Column(board_controls)],
              [sg.Text('Click anywhere on board for next move', font='_ 14')]]

    window = sg.Window('Chess', default_button_element_size=(12, 1), auto_size_buttons=False, icon='kingb.ico').Layout(
        layout)

    # ---===--- Loop taking in user input --- #
    whos_turn = -1
    fromm = None
    piece_from = None
    to = None
    Depth = 7
    started = False
    closed = False
    # redraw_board(window, boardx.board_layout)

    while True:

        if not started:
            button, value = window.Read() if whos_turn == 1 else window.Read(timeout=0)

        if button in (None, 'Start Game'):
            started = True

        if closed:
            break

        while started:

            button, value = window.Read() if whos_turn == 1 else window.Read(timeout=0)

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
                whos_turn = -1
                fromm = None
                piece_from = None
                started = False
                redraw_board(window, boardx.board_layout)



            elif not boardx.gameover and whos_turn == -1:

                moves = 0
                for i in boardx.black_pieces:
                    for j in i.legal_moves:
                        piece_from = i
                        move = j
                        moves += 1

                if moves > 1:
                    print("Thinking...")
                    piece_from, move, score = Minimax(boardx, Depth, -1, -1000000, 1000000)
                    print("FINAL:", score)

                piece_from = boardx.get_piece(piece_from.row, piece_from.col)
                frommm = copy.deepcopy([tuple((piece_from.row, piece_from.col))])
                to = move.to

                for x, y in move.eaten:
                    boardx.board_layout[x][y] = 0
                    boardx.white_pieces.remove(boardx.get_piece(x, y))

                boardx.move_to(piece_from, to[0], to[1])
                redraw_board(window, boardx.board_layout, to[0], to[1], frommm)
                check_game_state(boardx)
                print("Human's turn")

                fromm = None
                move = None
                to = None
                piece_from = None
                whos_turn = - whos_turn

            elif type(button) == type(()) and not boardx.gameover and whos_turn == 1:

                if (boardx.board_layout[button[0]][button[1]] == whos_turn or boardx.board_layout[button[0]][
                    button[1]] == 2 * whos_turn):
                    fromm = button
                    piece_from = boardx.get_piece(fromm[0], fromm[1])
                    redraw_board(window, boardx.board_layout, piece_from.row, piece_from.col,
                                 list(o.to for o in piece_from.legal_moves))

                if (boardx.board_layout[button[0]][button[1]] == 0) and fromm != None:

                    move = boardx.find_move(piece_from.legal_moves, button[0], button[1])

                    if move != None:

                        to = button

                        for x, y in move.eaten:
                            boardx.board_layout[x][y] = 0
                            boardx.black_pieces.remove(boardx.get_piece(x, y))

                        boardx.move_to(piece_from, to[0], to[1])
                        redraw_board(window, boardx.board_layout)
                        check_game_state(boardx)
                        print("Computer's turn")

                        fromm = None
                        move = None
                        to = None
                        piece_from = None
                        whos_turn = - whos_turn
