import PySimpleGUI as sg
import os
import chess
import chess.pgn
import copy
import time
import random
from Piece import Piece
from Board import Board
from Move import Move


button_names = ('close', 'cookbook', 'cpu', 'github', 'pysimplegui', 'run', 'storage', 'timer')

CHESS_PATH = '.'        # path to the chess pieces

BLANK = 0               # piece names
PAWNB = -1
PAWNW = 1
KINGB = -2
KINGW = 2


blank = os.path.join(CHESS_PATH, 'blank.png')
pawnB = os.path.join(CHESS_PATH, 'npawnb.png')
pawnW = os.path.join(CHESS_PATH, 'npawnw.png')
kingB = os.path.join(CHESS_PATH, 'nkingb.png')
kingW = os.path.join(CHESS_PATH, 'nkingw.png')

images = {PAWNB: pawnB, PAWNW: pawnW, KINGB: kingB, KINGW: kingW, BLANK: blank}



def Minimax(board, depth, team, alpha, beta):
    best_move = None
    best_move_piece = None
    done = False

    if team == 1:
        best_score = 1000000
        pieces = board.white_pieces
    else:
        best_score = -1000000
        pieces = board.black_pieces


    if depth < 1 or board.gameover:
        score = copy.deepcopy(board.score)
        return (None, None , score)

    for a,i in enumerate(pieces):
        if done:
            break
        for b,j in enumerate(i.legal_moves):

            board_save = copy.deepcopy(board)
            if team == 1:
                next_pos = board_save.white_pieces[a].legal_moves[b].to
                for x,y in j.eaten:
                    board_save.board[x][y] = 0
                    board_save.black_pieces.remove(board_save.get_piece(x,y))
                board_save.move_to(board_save.white_pieces[a], next_pos[0], next_pos[1])

            else:
                next_pos = board_save.black_pieces[a].legal_moves[b].to
                board_save.move_to(board_save.black_pieces[a], next_pos[0], next_pos[1])
                for x,y in j.eaten:
                    board_save.board[x][y] = 0
                    board_save.white_pieces.remove(board_save.get_piece(x,y))

            _, _, score = Minimax(board_save, depth - 1 , -team, alpha, beta)

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
                break


           



    return (best_move_piece, best_move, best_score)


def open_pgn_file(filename):
    pgn = open(filename)
    first_game = chess.pgn.read_game(pgn)
    moves = [move for move in first_game.main_line()]
    return moves

def render_square(image, key, location):
    
    if (location[0] + location[1]) % 2:
        color =  '#B58863'
    else:
        color = '#F0D9B5'
    return sg.RButton('', image_filename=image, size=(1, 1), button_color=('white', color), pad=(0, 0), key=key)

def redraw_board(window, board, row = 10 ,col = 10, moves = (10,10)):
    for i in range(8):
        for j in range(8):
            color = '#B58863' if (i+j) % 2 else '#F0D9B5'
            if moves.count((i,j)) != 0:
                print("ok")
                color = '#A58888'
            if i == row and col == j:
                color = '#B46888'
            piece_image = images[board[i][j]]
            elem = window.FindElement(key=(i,j))
            elem.Update(button_color = ('white', color),
                        image_filename=piece_image,)







def PlayGame(boardx):


    menu_def = [['&File', ['&Open PGN File', 'E&xit' ]],
                ['&Help', '&About...'],]

    # sg.SetOptions(margins=(0,0))
    sg.ChangeLookAndFeel('GreenTan')
    # create initial board setup
    # the main board display layout
    board_layout = [[sg.T('     ')] + [sg.T('{}'.format(a), pad=((23,27),0), font='Any 13') for a in 'abcdefgh']]
    # loop though board and create buttons with images
    for i in range(8):
        row = [sg.T(str(8-i)+'   ', font='Any 13')]
        for j in range(8):
            piece_image = images[boardx.board[i][j]]
            row.append(render_square(piece_image, key=(i,j), location=(i,j)))
        row.append(sg.T(str(8-i)+'   ', font='Any 13'))
        board_layout.append(row)
    # add the labels across bottom of board
    board_layout.append([sg.T('     ')] + [sg.T('{}'.format(a), pad=((23,27),0), font='Any 13') for a in 'abcdefgh'])

    board_controls = [[sg.RButton('New Game', key='Open PGN File'), sg.RButton('Draw')],
                      [sg.RButton('Resign Game')],
                      [sg.CBox('Play as White', key='_white_')],
                      [sg.Text('Move List')],
                      [sg.Multiline([], do_not_clear=True, autoscroll=True, size=(15,10),key='_movelist_')],]


    board_tab = [[sg.Column(board_layout)]]

    # the main window layout
    layout = [[sg.Menu(menu_def, tearoff=False)],
              [sg.TabGroup([[sg.Tab('Board',board_tab),
                             
                             ]], title_color='red'),
               sg.Column(board_controls)],
              [sg.Text('Click anywhere on board for next move', font='_ 14')]]

    window = sg.Window('Chess', default_button_element_size=(12,1), auto_size_buttons=False, icon='kingb.ico').Layout(layout)

    # ---===--- Loop taking in user input --- #
    i = 0
    moves = None
    whos_turn = -1
    fromm = None
    piece_from = None
    to = None

    while True:

        button, value = window.Read()


        #can_play = boardx
        if not boardx.gameover and whos_turn == -1: 

            piece_from, move , score = Minimax(boardx , 8 ,-1,-1000000,1000000)
            print("FINAL:",score)

            piece_from = boardx.get_piece(piece_from.row,piece_from.col)
                            
            to = move.to
            for x,y in move.eaten:
                j = boardx.get_piece(x,y)
                boardx.board[j.row][j.col] = 0
                if whos_turn == 1:
                    boardx.black_pieces.remove(boardx.get_piece(j.row,j.col))
                else:
                    boardx.white_pieces.remove(boardx.get_piece(j.row,j.col))

            boardx.move_to(piece_from,to[0],to[1])
            redraw_board(window, boardx.board)
            fromm = None
            move = None
            to = None
            piece_from = None
            whos_turn = - whos_turn


        elif button in (None, 'Exit'):
            break


        elif type(button) == type(()) and not boardx.gameover and whos_turn == 1:

                if(boardx.board[button[0]][button[1]] == whos_turn or boardx.board[button[0]][button[1]] == 2 * whos_turn):
                    
                    fromm = button
                    piece_from = boardx.get_piece(fromm[0],fromm[1])
                    redraw_board(window, boardx.board , piece_from.row, piece_from.col,list(o.to for o in piece_from.legal_moves))

                if(boardx.board[button[0]][button[1]] == 0) and fromm != None:
                    
                    move = boardx.find_move(piece_from.legal_moves, button[0], button[1])

                    if move != None:

                        to = button

                        for x,y in move.eaten:
                            boardx.board[x][y] = 0

                            if whos_turn == 1:
                                boardx.black_pieces.remove(boardx.get_piece(x,y))
                            else:
                                boardx.white_pieces.remove(boardx.get_piece(x,y))

                        boardx.move_to(piece_from,to[0],to[1])


                        redraw_board(window, boardx.board)

                        fromm = None
                        move = None
                        to = None
                        piece_from = None
                        whos_turn = - whos_turn

                    
                    
 

                 
                    

        elif boardx.gameover:

            if boardx.winner == 0:
                print("DRAW!!")
            if boardx.winner == 1:
                print("White Wins!!")
            if boardx.winner == -1:
                print("Black Wins!!")
'''
        if moves is not None and i < len(moves):

            move = moves[i]                 # get the current move
            window.FindElement('_movelist_').Update(value='{}   {}\n'.format(i+1, str(move)), append=True)
            move_from = move.from_square    # parse the move-from and move-to squares
            move_to = move.to_square
            row, col = move_from // 8, move_from % 8
            piece = board[row][col]         # get the move-from piece
            button = window.FindElement(key=(row,col))
            for x in range(3):
                button.Update(button_color = ('white' , 'red' if x % 2 else 'white'))
                window.Refresh()
                time.sleep(.05)
            board[row][col] = BLANK         # place blank where piece was
            row, col = move_to // 8, move_to % 8  # compute move-to square
            board[row][col] = piece         # place piece in the move-to square
            redraw_board(window, board)
            i += 1

'''