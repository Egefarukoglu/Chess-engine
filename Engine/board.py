WHITE = 'w'
BLACK = 'b'

PAWN = 'P'
KNIGHT = 'N'
BISHOP = 'B'
ROOK = 'R'
QUEEN = 'Q'
KING = 'K'

class Move:
    def __init__(self ,from_square , to_square ,board , promotion=None , is_castle=False , castle_side=None , is_en_passant=False):
        self.from_square = from_square
        self.to_square = to_square
        self.piece_move = board.square[from_square]
        self.piece_captured = board.square[to_square]
        self.promotion = promotion
        self.is_castle = is_castle
        self.castle_side = castle_side # 'KS' OR 'QS
        self.is_en_passant = is_en_passant
        self.prev_en_passant = board.en_passant_square # it stores the previous en passant square for undo_move() to restore it correctly
        self.prev_castling_rights = board.castling_rights.copy() # it stores the previous castling rights for undo_move() to restore it correctly

class Board:
    def __init__(self):
        self.square = ['bR' , 'bN' , 'bB' , 'bQ' , 'bK' , 'bB' , 'bN' , 'bR' ,
                       'bP' , 'bP' , 'bP' , 'bP' , 'bP' , 'bP' , 'bP' , 'bP' , 
                       '--' , '--' , '--' , '--' , '--' , '--' , '--' , '--' ,
                       '--' , '--' , '--' , '--' , '--' , '--' , '--' , '--' ,
                       '--' , '--' , '--' , '--' , '--' , '--' , '--' , '--',
                       '--' , '--' , '--' , '--' , '--' , '--' , '--' , '--' ,
                       'wP' , 'wP' , 'wP' , 'wP' , 'wP' , 'wP' , 'wP' , 'wP' ,
                       'wR' , 'wN' , 'wB' , 'wQ' , 'wK' , 'wB' , 'wN' , 'wR']
        self.move_side = WHITE
        self.all_moves = []
        self.piece_symbols ={'wP': '♙' , 'wN': '♘' , 'wB': '♗' , 'wR': '♖' , 'wQ': '♕' , 'wK':'♔'
                             , 'bP': '♟' , 'bN': '♞' , 'bB': '♝' , 'bR': '♜' , 'bQ' : '♛' , 'bK':'♚'}
        self.king_positions = {'w': 60 , 'b': 4}
        
        self.en_passant_square = None
        self.castling_rights = {'wKS': True , 'wQS': True , 'bKS': True , 'bQS': True}


    def make_move(self , move):
        self.square[move.to_square] = move.piece_move
        self.square[move.from_square] = '--'
        piece = move.piece_move

        # update castling rights and move rook if it's a castling move
        if move.is_castle:
            if move.castle_side == 'KS': 
                 if piece[0] == WHITE:
                    self.square[61] = 'wR'; self.square[63] = '--' # move the rook for white king side castling
                 else:
                    self.square[5]  = 'bR'; self.square[7]  = '--' # move the rook for black king side
            elif move.castle_side == 'QS':
                if piece[0] == WHITE:
                    self.square[59] = 'wR'; self.square[56] = '--'# move the rook for white queen side castling
                else:
                    self.square[3]  = 'bR'; self.square[0]  = '--'# move the rook for black queen side castling

        if move.piece_move == 'wK':
            self.castling_rights['wKS'] = False
            self.castling_rights['wQS'] = False
            self.king_positions['w'] = move.to_square

        elif move.piece_move == 'bK':
            self.castling_rights['bKS'] = False
            self.castling_rights['bQS'] = False
            self.king_positions['b'] = move.to_square
        elif move.piece_move == 'wR':
            if move.from_square == 63:
                self.castling_rights['wKS'] = False
            elif move.from_square == 56:
                self.castling_rights['wQS'] = False
        elif move.piece_move == 'bR':
            if move.from_square == 7:
                self.castling_rights['bKS'] = False
            elif move.from_square == 0:
                self.castling_rights['bQS'] = False

        # en passant capture
        if move.is_en_passant:
            captured_pawn_sq = move.to_square + (8 if piece[0] == WHITE else -8)
            self.square[captured_pawn_sq] = '--'

        # Update en passant square
        if piece[1] == PAWN and abs(move.to_square - move.from_square) == 16:
            self.en_passant_square = (move.to_square + move.from_square) // 2
        
        else:
            self.en_passant_square = None

        if piece[1] == PAWN and move.to_square == self.en_passant_square:
            captured_pawn_square = move.to_square - (8 if piece[0] == 'w' else -8)
            self.square[captured_pawn_square] = '--'

        # Update promotion
        if move.promotion:
            self.square[move.to_square] = piece[0] + move.promotion

        self.all_moves.append(move)
        self.move_side = 'b' if self.move_side == 'w' else 'w' 

    # Undo the last move made on the board
    def undo_move(self):
        if not self.all_moves:
            return
        
        move = self.all_moves.pop()
        self.square[move.from_square] = move.piece_move
        self.square[move.to_square] = move.piece_captured

        # Restore the king's position if it was moved
        if move.piece_move[1] == KING:
            self.king_positions[move.piece_move[0]] = move.from_square

        # Restore the rook if it was a castling move
        if move.is_castle:
            if move.castle_side == 'KS':
                if move.piece_move[0] == WHITE:
                    self.square[63] == 'wR' ; self.square[61] == '--'

                else:
                    self.square[7] == 'bR' ; self.square[5] == '--'

            elif move.castle_side == 'QS':
                if move.piece_move[0] == WHITE:
                    self.square[56] == 'wR' ; self.square[59] == '--'

                else:
                    self.square[0] == 'bR' ; self.square[3] == '--'

        # Restore a captured pawn if it was an after en passant undo
        if move.is_en_passant:
            opponent  = BLACK if move.piece_move[0] == WHITE else WHITE
            cap_sq    = move.to_square + (8 if move.piece_move[0] == WHITE else -8)
            self.square[cap_sq] = opponent + PAWN

        # Restore snapshots
        self.en_passant_square  = move.prev_en_passant
        self.castling_rights    = move.prev_castling_rights.copy()
        self.move_side          = BLACK if self.move_side == WHITE else WHITE

    def reset_board(self):
        self.__init__()  