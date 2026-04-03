from board import Board , Move , PAWN , KNIGHT , BISHOP , ROOK , QUEEN , KING

# define move sets for each piece

Knight_Moveset = [17 , 15 , 10 , 6 , -17 , -15 , -10 , -6]
Rook_Moveset = [8 , -8 , 1 , -1]
Bishop_Moveset = [9 , 7 , -9 , -7]
Queen_moveset = Rook_Moveset + Bishop_Moveset
King_moveset = Queen_moveset

class Generate_Moves:
    def __init__(self , board: Board):
        self.board = board

    def find_row(self , square):
        return square // 8
    
    def find_col(self , square):
        return square % 8
    
    def is_valid_square(self , square):
        return 0 <= square < 64
    
    # Generating moves for each piece type   
    def generate_pawn_moves(self , square):
        possible_moves = []
        color = piece[0]
        piece = self.board.square[square]

        row , col = square // 8 , square % 8
        direction = -1 if color == 'w' else 1
        start_row = 6 if color == 'w' else 1
        promotion_row = 0 if color == 'w' else 7

        # single move forward
        forward = square + direction * 8
        if self.is_valid_square(forward) and self.board.square[forward] == '--':
            self.add_pawn_moves(possible_moves , square , forward , color , promotion_row)

        # double move forward
        if row == start_row:
            double_forward = square + direction * 16
            if self.is_valid_square(double_forward) and self.board.square[forward] == '--' and self.board.square[double_forward] == '--':
                possible_moves.append(double_forward)

        # captures
        for capture in [1 , -1]:
            target_col = col + capture
            if 0 <= target_col < 8:
                target_square = square + direction * 8 + capture
                if self.is_valid_square(target_square):
                    target_piece = self.board.square[target_square]
                    if target_piece != '--' and target_piece[0] != color:
                        self.add_pawn_moves(possible_moves , square , target_square , promotion_row)

                    # en passant
                    elif target_square == self.board.en_passant_square:
                        self.add_pawn_moves(possible_moves , square , target_square , promotion_row)

        return possible_moves
    
    # this funtion decides whether the pawn move is a promotion move or not and adds the promotion piece to the move if it is a promotion move
    def add_pawn_moves(self , moves , start_square , target_square ,color, promotion_row):
        if target_square // 8 == promotion_row:
            for promo_piece in ['Q' , 'R' , 'B' , 'N']:
                new_move = Move(self.board , start_square , target_square , promotion=promo_piece)
                moves.append(new_move)
        else:
            new_move = Move(start_square , target_square)
            moves.append(new_move)

    # generate moves for Kngight
    def generate_knight_moves(self , square):
        possible_moves = []
        piece = self.board.square[square]
        start_row = self.find_row(square)
        start_col = self.find_col(square)

        for move in Knight_Moveset:
            target_square = square + move
            target_row = self.find_row(target_square)
            target_col = self.find_col(target_square)

            if not self.is_valid_square(target_square):
                continue

            if abs(start_row - target_row) == 2 and abs(start_col - target_col) == 1 or abs(start_row - target_row) == 1 and abs(start_col - target_col) == 2:
                target_piece = self.board.square[target_square]
                if target_piece == '--' or target_piece[0] != piece[0]:
                    possible_moves.append(Move(square , target_square , self.board))

        return possible_moves
                
    # generate moves for bishop
    def generate_bishop_moves(self , square):
        possible_moves = []  
        piece = self.board.square[square]
        start_row = self.find_row(square)
        start_col = self.find_col(square)

        for move in Bishop_Moveset:
            target_square = square + move
            while self.is_valid_square(target_square):
                target_piece = self.board.square[target_square]
                new_row = self.find_row(target_square)
                new_col = self.find_col(target_square)
            
                if abs(start_row - new_row) == abs(start_col - new_col):
                    if target_piece == '--':
                        possible_moves.append(target_square)

                    elif target_piece[0] != piece[0]:
                        possible_moves.append(target_square)
                        break

                    else:
                        break
                target_square += move

        return possible_moves

    # generate moves for rook
    def generate_rook_moves(self , square):
        possible_moves = []
        piece = self.board.square[square]
        start_row = self.find_row(square)
        start_col = self.find_col(square)

        for move in Rook_Moveset:
            target_square = square + move
            while self.is_valid_square(target_square):
                target_piece = self.board.square[target_square]
                new_row = self.find_row(target_square)
                new_col = self.find_col(target_square)

                if start_row == new_row or start_col == new_col:
                    if target_piece == '--':
                        possible_moves.append(target_square)

                    elif target_piece[0] != piece[0]:
                        possible_moves.append(target_square)
                        break

                    else:
                        break
                target_square += move

        return possible_moves


    # Generate moves for Queen
    def generate_queen_moves(self , square):
        possible_moves = []
        piece = self.board.square[square]
        start_row = self.find_row(square)
        start_col = self.find_col(square)

        for move in Queen_moveset:
            target_square = square + move
            while self.is_valid_square(target_square):
                target_piece = self.board.square[target_square]
                new_row = self.find_row(target_square)
                new_col = self.find_col(target_square)

                if start_row == new_row or start_col == new_col or abs(start_row - new_row) == abs(start_col - new_col):
                    if target_piece == '--':
                        possible_moves.append(target_square)
                        
                    
                    elif target_piece[0] != piece[0]:
                        possible_moves.append(target_square)
                        break
                    else:
                        break
                target_square += move
                
        return possible_moves
    
    # Generate moves for King
    def generate_king_moves(self , square):
        possible_moves = []
        piece = self.board.square[square]
        start_row = self.find_row(square)
        start_col = self.find_col(square)

        for move in King_moveset:
            target_square = square + move

            if self.is_valid_square(target_square):
                target_piece = self.board.square[target_square]
                new_row = self.find_row(target_square)
                new_col = self.find_col(target_square)

                if abs(start_row - new_row) <= 1 and abs(start_col - new_col) <= 1:
                    if target_piece == '--' or target_piece[0] != piece[0]:
                        possible_moves.append(target_square)
        return possible_moves
    

    def generate_all_moves(self , square):
        # Generate moves for all pieces on the board
        piece = self.board.square[square]
        if piece == '--' or piece[0] != self.board.move_side:
            return []
        
        piece_type = piece[1]
        if piece_type == 'P':
            return self.generate_pawn_moves(square)
        
        elif piece_type == 'N':
            return self.generate_knight_moves(square)
        
        elif piece_type == 'B':
            return self.generate_bishop_moves(square)
        
        elif piece_type == 'R':
            return self.generate_rook_moves(square)
        
        elif piece_type == 'Q':
            return self.generate_queen_moves(square)
        
        elif piece_type == 'K':
            return self.generate_king_moves(square)
        
        return []