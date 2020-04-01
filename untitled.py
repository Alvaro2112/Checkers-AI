           '''
                    available_pieces = [] 

                    for o in boardx.black_pieces:
                        if len(o.legal_moves) != 0 : available_pieces += [o]

                    piece_from = random.choice(available_pieces)
                    fromm = (piece_from.row,piece_from.col)

                    #redraw_board(window, boardx.board , piece_from.row, piece_from.col,list(o.to for o in piece_from.legal_moves))

                    move = random.choice(piece_from.legal_moves)

                    to = (move.to)

                    for j in move.eaten:
                            boardx.board[j.row][j.col] = 0
                            if whos_turn == 1:
                                boardx.black_pieces.remove(boardx.get_piece(j.row,j.col))
                            else:
                                boardx.white_pieces.remove(boardx.get_piece(j.row,j.col))
                    piece_from.move_to(to[0],to[1])
                    redraw_board(window, boardx.board)
                    fromm = None
                    move = None
                    to = None
                    piece_from = None
                    whos_turn = - whos_turn

                 ''' 
                 ''' 
                   piece_from, move , _ = Minimax(boardx , 1)
                    to = move.to
                    piece_from.move_to(to[0],to[1])

                    redraw_board(window, boardx.board)
                    fromm = None
                    move = None
                    to = None
                    piece_from = None
                    whos_turn = - whos_turn
                '''

                    piece_from, move , _ = Minimax(boardx , 2 ,-1)

                    piece_from = boardx.get_piece(piece_from.row,piece_from.col)
                    
                    to = move.to
                    for x,y in move.eaten:
                            j = boardx.get_piece(x,y)
                            boardx.board[j.row][j.col] = 0
                            if whos_turn == 1:
                                boardx.black_pieces.remove(boardx.get_piece(j.row,j.col))
                            else:
                                boardx.white_pieces.remove(boardx.get_piece(j.row,j.col))

                    piece_from.move_to(to[0],to[1])

                    redraw_board(window, boardx.board)
                    fromm = None
                    move = None
                    to = None
                    piece_from = None
                    whos_turn = - whos_turn








                     available_pieces = [] 

                    for o in boardx.black_pieces:
                        if len(o.legal_moves) != 0 : available_pieces += [o]

                    piece_from = random.choice(available_pieces)
                    fromm = (piece_from.row,piece_from.col)

                    #redraw_board(window, boardx.board , piece_from.row, piece_from.col,list(o.to for o in piece_from.legal_moves))

                    move = random.choice(piece_from.legal_moves)

                    to = (move.to)

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