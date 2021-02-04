import chess as chess
import chess.polyglot

class Game:
    """ Class for a chess game."""
    def __init__(self, gameID, opponent="", color="white"):
        self.gameID = gameID
        self.opponent = opponent
        self.color = color
        self.board = chess.Board()

    def select_move(depth, turn):
        bestMove = chess.Move.null()
        bestValue = -float('inf')

        for move in self.board.legal_moves:
            make_mov(move,self.board)
            boardValue = minmax(self.board,depth-1,-float('inf'),float('inf'), not turn)
            unmake_move(self.board)
            if boardValue >= bestValue:
                bestValue = boardValue
                bestMove = move
        
        return bestMove.uci()

    def make_move(move):