# Author: Steve Hoang
# GitHub username: steveh0ang
# Date: 02/25/25
# Description: Abstract board game based on chess known as King of the Hill.

class ChessVar:
    def __init__(self):
        """
        Initializes the board for King of the Hill chess variant.
        """
        self.__game_state = "UNFINISHED"
        # White moves first
        self.__turn = "white"
        # 8x8 chess board layout, lowercase = black chess pieces, uppercase = white chess pieces
        self.__board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],   # row 8 / index 0
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],   # row 7 / index 1
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],   # row 6 / index 2
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],   # row 5 / index 3
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],   # row 4 / index 4
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],   # row 3 / index 5
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],   # row 2 / index 6
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']    # row 1 / index 7
        ]
        self.__center_squares = {'d4', 'e4', 'd5', 'e5'}    # winning squares

    def get_game_state(self):
        """
        Returns the current game status with the following: 'UNFINISHED', 'WHITE_WON', or 'BLACK_WON'.
        """
        return self.__game_state

    def get_board(self):
        """
        Returns the chess board as a nested list.
        """
        return self.__board

    def print_board(self):
        """
        Prints the chess board and replaces the empty space with an underscore ('_') for readability.
        """
        board = self.get_board()
        for row in board:
            # replaces the space with '_' to make the board easier to read
            for piece in row:
                if piece == ' ':
                    print('_', end=' ')
                else:
                    print(piece, end=' ')
            print("")

    def notation_conversion(self, pos):
        """
        Converts chess board notation to coordinates for nested list.
        """
        # checks if the position is legal
        if type(pos) != str:
            raise ValueError("The position entered must be a string.")
        if len(pos) < 2:
            raise ValueError("The position entered must be at least two characters.")

        # checks for valid position entered for column
        columns = "abcdefgh"
        if pos[0] not in columns:
            raise ValueError("The position entered must be a letter from 'a' to 'h.'")
        col = columns.index(pos[0]) # converts column alphabet notation to index (a is 0, b is 1, etc.)

        # Checks for valid position entered for row
        if not pos[1].isdigit():
            raise ValueError("The position entered must be a number.")
        row = 8 - int(pos[1]) # converts row number notation to index (row 1 is index 7, row 8 is index 0)
        if row <0 or row > 7:
            raise ValueError("The position entered must be between 1 and 8.")

        return row, col

    def pawn_move(self, piece, row1, col1, row2, col2):
        """
        Checks if all pawn moves are legal.
        """
        if piece.isupper(): # white chess piece
            direction = -1  # moves up
            start_row = 6   # white pawns starts on row 6
        else:   # black chess piece
            direction = 1   # moves down
            start_row = 1   # white pawns starts on row 1

        move_forward = col1 == col2 # stay in same coloumn
        move_one_row = row2 == row1 + direction # move one row forward
        empty_square = self.__board[row2][col2] == ' '  # checks if square is empty
        if move_forward and move_one_row and empty_square:
            return True

        # pawns can move 2 squares from starting position
        at_start_row = row1 == start_row    # pawn starting position
        move_two_rows = row2 == row1 + 2 * direction    # pawn moves 2 squares forward from starting position
        middle_empty_square = self.__board[row2 + direction][col1] == ' '   # middle square is empty
        if move_forward and at_start_row and move_two_rows and middle_empty_square and empty_square:
            return True

        # pawn can move diagonally to capture chess piece
        move_one_column = abs(col2 - col1) == 1 # move to the left or right column
        not_empty_square = self.__board[row2][col2] != ' ' # square is occupied with a chess piece
        capture_square = self.__board[row2][col2].isupper() != piece.isupper() # chess piece belongs to opponent
        if move_one_column and move_one_row and not_empty_square and capture_square:
            return True

        return False    #else, move is illegal

    def king_move(self, piece, row1, col1, row2, col2):
        """
        Checks if all king moves are legal.
        """
        diff_row = abs(row2 - row1)
        diff_col = abs(col2 - col1)

        # Kings are allowed to move one square in any directions
        return (diff_row <= 1 and diff_col <= 1) and not (diff_row == 0 and diff_col == 0)

    def queen_move(self, piece, row1, col1, row2, col2):
        """
        Checks if all queen moves are legal.
        """
        diff_row = row2 - row1
        diff_col = col2 - col1

        # queen can move to any square on the current row
        if diff_row == 0:
            step = 1 if diff_col > 0 else -1
            for col in range(col1, + step, col2 + 1):
                if self.__board[row1][col] != ' ':  # checks if a chess piece is blocking
                    return False
            return True

        # queen can move to any square in the current column
        if diff_col == 0:
            step = 1 if diff_row > 0 else -1
            for row in range(row1 + step, row2 + 1):
                if self.__board[row][col1] != ' ':  # checks if a chess piece is blocking
                    return False
            return True

        # queen can move to any square diagonally
        if abs(diff_row) == abs(diff_col):
            row_step = 1 if diff_row > 0 else -1
            col_step = 1 if diff_col > 0 else -1
            row, col = row1 + row_step, col1 + col_step
            while row != row2 and col != col2:
                if self.__board[row][col] != ' ':   # checks if a chess piece is blocking
                    return False
                row += row_step
                col += col_step
            return True

    def bishop_move(self, piece, row1, col1, row2, col2):
        """
        Checks if all bishop moves are legal.
        """
        diff_row = row2 - row1
        diff_col = col2 - col1

        if abs(diff_row) == abs(diff_col):
            row_step = 1 if diff_row > 0 else -1
            col_step = 1 if diff_col > 0 else -1
            row, col = row1 + row_step, col1 + col_step
            while row != row2 and col != col2:
                if self.__board[row][col] != ' ':   # checks if a chess piece is blocking
                    return False
                row += row_step
                col += col_step
            return True

    def knight_move(self, piece, row1, col1, row2, col2):
        """
        Checks if all knight moves are legal.
        """
        diff_row = abs(row2 - row1)
        diff_col = abs(col2 - col1)

        # knights can move in L shape
        return (diff_row == 2 and diff_col == 1) or (diff_row == 1 and diff_col == 2)

    def rook_move(self, piece, row1, col1, row2, col2):
        """
        Checks if all rook moves are legal.
        """
        diff_row = row2 - row1
        diff_col = col2 - col1

        # rook can move to any square on the current row
        if diff_row == 0:
            step = 1 if diff_col > 0 else -1
            for col in range(col1 + step, col2, step):
                if self.__board[row2][col] != ' ':  # checks if a chess piece is blocking
                    return False
            return True

        # rook can move to any square in the current column
        if diff_col == 0:
            step = 1 if diff_row > 0 else -1
            for row in range(row1 + step, row2, step):
                if self.__board[row][col1] != ' ':  # checks if a chess piece is blocking
                    return False
            return True

    def make_move(self, pos1, pos2):
        """
        Check if chess piece move from position 1 to position 2 is legal.
        """
        # checks game state
        if self.__game_state != "UNFINISHED":
            return False

        # converts chess board notation to indices
        row1, col1 = self.notation_conversion(pos1)
        row2, col2 = self.notation_conversion(pos2)

        # check if chosen position has a chess piece (pos1)
        piece = self.__board[row1][col1]

        if piece == ' ':
            return False

        # checks if player chooses the correct chess piece color
        if self.__turn == "white":  # white chess piece is uppercase
            if piece.islower():
                return False
        if self.__turn == "black":  # black chess piece is lowercase
            if piece.isupper():
                return False

        # moveset for each chess piece type
        if piece in ('P', 'p'):
            if not self.pawn_move(piece, row1, col1, row2, col2):
                return False
        elif piece in ('K', 'k'):
            if not self.king_move(piece, row1, col1, row2, col2):
                return False
        elif piece in ('Q', 'q'):
            if not self.queen_move(piece, row1, col1, row2, col2):
                return False
        elif piece in ('B', 'b'):
            if not self.bishop_move(piece, row1, col1, row2, col2):
                return False
        elif piece in ('N', 'n'):
            if not self.knight_move(piece, row1, col1, row2, col2):
                return False
        elif piece in ('R', 'r'):
            if not self.rook_move(piece, row1, col1, row2, col2):
                return False
        else:
            return False

        # win condition by reaching center squares with king chess piece or captured kings
        target = self.__board[row2][col2]
        self.__board[row2][col2] = piece
        self.__board[row1][col1] = ' '

        if target in ('K', 'k'):    # win condition by captured kings
            self.__game_state = "WHITE_WON" if self.__turn == "white" else "BLACK_WON"
        elif piece in ('K', 'k') and pos2 in self.__center_squares: # win condition by reaching center squares
            self.__game_state = "WHITE_WON" if self.__turn == "white" else "BLACK_WON"
        else:
            self.__turn = "black" if self.__turn == "white" else "white"

        return True

# game = ChessVar()
# print(game.make_move('d2', 'd4'))
# print(game.make_move('g7', 'g5'))
# print(game.make_move('c1', 'g5'))
# print(game.make_move('e7', 'e6'))
# print(game.make_move('g5', 'd8'))
# board = game.get_board()
# print('[')
# for row in board:
#     print(f' {row},')
# print(']')