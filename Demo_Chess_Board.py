import PySimpleGUI as sg
import os
import chess
import chess.pgn
import copy
import time

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

images = {PAWNB: pawnB, PAWNW: pawnW,KINGB: kingB, KINGW: kingW, BLANK: blank}

def open_pgn_file(filename):
    pgn = open(filename)
    first_game = chess.pgn.read_game(pgn)
    moves = [move for move in first_game.main_line()]
    return moves

def render_square(image, key, location, listt,row,col):
    
    if location[0] == row and location[1] == col:
        color =  '#B46888'
        return sg.RButton('', image_filename=image, size=(1, 1), button_color=('white', color), pad=(0, 0), key=key)

    for i in listt:
        if i.to == (location[0],location[1]):
            color =  '#A58888'
            return sg.RButton('', image_filename=image, size=(1, 1), button_color=('white', color), pad=(0, 0), key=key)
    
    

    if (location[0] + location[1]) % 2:
        color =  '#B58863'
    else:
        color = '#F0D9B5'
    return sg.RButton('', image_filename=image, size=(1, 1), button_color=('white', color), pad=(0, 0), key=key)

def redraw_board(window, board):
    for i in range(8):
        for j in range(8):
            color = '#B58863' if (i+j) % 2 else '#F0D9B5'
            piece_image = images[board[i][j]]
            elem = window.FindElement(key=(i,j))
            elem.Update(button_color = ('white', color),
                        image_filename=piece_image,)


def PlayGame(initial_board, listt, rowww, colll):

    menu_def = [['&File', ['&Open PGN File', 'E&xit' ]],
                ['&Help', '&About...'],]

    # sg.SetOptions(margins=(0,0))
    sg.ChangeLookAndFeel('GreenTan')
    # create initial board setup
    board = copy.deepcopy(initial_board)
    # the main board display layout
    board_layout = [[sg.T('     ')] + [sg.T('{}'.format(a), pad=((23,27),0), font='Any 13') for a in 'abcdefgh']]
    # loop though board and create buttons with images
    for i in range(8):
        row = [sg.T(str(8-i)+'   ', font='Any 13')]
        for j in range(8):
            piece_image = images[board[i][j]]
            row.append(render_square(piece_image, key=(i,j), location=(i,j), listt = listt, row=rowww, col=colll))
        row.append(sg.T(str(8-i)+'   ', font='Any 13'))
        board_layout.append(row)
    # add the labels across bottom of board
    board_layout.append([sg.T('     ')] + [sg.T('{}'.format(a), pad=((23,27),0), font='Any 13') for a in 'abcdefgh'])

    board_controls = [[sg.RButton('New Game', key='Open PGN File'), sg.RButton('Draw')],
                      [sg.RButton('Resign Game')],
                      [sg.CBox('Play a White', key='_white_')],
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
    while True:
        button, value = window.Read()
        

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

