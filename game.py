import chess as chess
import chess.polyglot

class ChessGame:
    """ Class for a chess game."""
    def __init__(self, gameID, gameFull):
        self.gameID = gameID
        self.gameFull = gameFull
        self.board = chess.Board()
        self.isWhite = True
        self.turn = 0
        self.lastmove = ''

    def select_move(self, depth, turn):
        bestMove = chess.Move.null()
        bestValue = -float('inf')

        for move in self.board.legal_moves:
            self.make_move(move)
            boardValue = minmax(self.board,depth-1,-float('inf'),float('inf'), not turn)
            unmake_move(self.board)
            if boardValue >= bestValue:
                bestValue = boardValue
                bestMove = move
        
        return bestMove.uci()

    def make_move(self, move):
        # TODO
        print('TODO make move')

    def accept_draw(self):
        # TODO
        print('TODO check if draw should be accepted.')
        return False