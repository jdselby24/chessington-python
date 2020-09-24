"""
Definitions of each of the different chess pieces.
"""

from abc import ABC, abstractmethod

from chessington.engine.data import Player, Square

class Piece(ABC):
    """
    An abstract base class from which all pieces inherit.
    """

    def __init__(self, player):
        self.player = player
        self.moved = False

    @abstractmethod
    def get_available_moves(self, board):
        """
        Get all squares that the piece is allowed to move to.
        """
        pass

    def move_to(self, board, new_square):
        self.moved = True
        """
        Move this piece to the given square on the board.
        """
        current_square = board.find_piece(self)
        board.move_piece(current_square, new_square)

    def pieceCapturable(self, piece):
        return piece.player != self.player

    def isCapturable(self, board, square):
        return (board.squareInBounds(square) and not board.squareEmpty(square) and self.pieceCapturable(board.get_piece(square)))

    def isFreeOrCapturable(self, board, square):
        return board.squareInBounds(square) and (board.squareEmpty(square) or self.pieceCapturable(board.get_piece(square)))

class Pawn(Piece):
    """
    A class representing a chess pawn.
    """

    def get_available_moves(self, board):
        
        positionDelta = 0
        currentLoc = board.find_piece(self)

        if self.player == Player.WHITE: 
            positionDelta = 1 
        else:
            positionDelta = -1

        single_move = Square.at(currentLoc.row + positionDelta, currentLoc.col)
        double_move = Square.at(currentLoc.row + positionDelta * 2, currentLoc.col)

        diagonal_move_1 = Square.at(currentLoc.row + positionDelta, currentLoc.col + positionDelta)
        diagonal_move_2 = Square.at(currentLoc.row + positionDelta, currentLoc.col - positionDelta)

        

        # Standard Forward moves
        moves = []
        if board.squareInBounds(single_move) and board.squareInBounds(double_move):

            if board.get_piece(single_move) is None:
                moves.append(single_move)

                if (board.get_piece(double_move) is None) and not self.moved:
                    moves.append(double_move)

        capturingMoves = []
        if board.squareInBounds(diagonal_move_1) and board.squareInBounds(diagonal_move_2):
            piece1 = board.get_piece(diagonal_move_1)
            piece2 = board.get_piece(diagonal_move_2)

            if piece1 is not None and piece1.player != self.player:
                capturingMoves.append(diagonal_move_1)

            if piece2 is not None and piece2.player != self.player:
                capturingMoves.append(diagonal_move_2)

        return moves + capturingMoves


class Knight(Piece):
    """
    A class representing a chess knight.
    """

    def get_available_moves(self, board):
        loc = board.find_piece(self)
        row, col = loc.row, loc.col

        possibleMoves = [
            Square.at(row + 2, col + 1), 
            Square.at(row + 2, col - 1),
            Square.at(row + 1, col + 2), 
            Square.at(row + 1, col - 2),
            Square.at(row - 2, col + 1),
            Square.at(row - 2, col - 1),
            Square.at(row - 1, col + 2), 
            Square.at(row - 1, col - 2)
        ]

        validMoves = []
        for move in possibleMoves:
            if(self.isFreeOrCapturable(board, move)):
                validMoves.append(move)

        return validMoves

class Bishop(Piece):
    """
    A class representing a chess bishop.
    """

    def get_available_moves(self, board):
        return []


class Rook(Piece):
    """
    A class representing a chess rook.
    """

    def get_available_moves(self, board):
        return []


class Queen(Piece):
    """
    A class representing a chess queen.
    """

    def get_available_moves(self, board):
        return []


class King(Piece):
    """
    A class representing a chess king.
    """

    def get_available_moves(self, board):
        return []