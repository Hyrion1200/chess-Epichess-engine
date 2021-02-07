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
        self.boardvalue = 0

    def select_move(self, depth, turn):
        print("selectmove")
        bestMove = chess.Move.null()
        bestValue = -float('inf')

        for move in self.board.legal_moves:
            self.make_move(move)
            boardValue = self.__minmax(self.board,depth-1,-float('inf'),float('inf'), not turn)
            self.unmake_move(self.board)
            if boardValue >= bestValue:
                bestValue = boardValue
                bestMove = move
        print(self.board)
        print(bestValue)
        return bestMove.uci()

    def make_move(self, move):
        self.__update_eval(move,self.board.turn)
        self.board.push(move)
        return move
    
    def unmake_move(self,board):
        mov = board.pop()
        self.__update_eval(mov,not board.turn)
        return mov

    def get_move(self):
        move = self.select_move(4,self.board.turn)
        print(move + " has been played")
        print(self.board)
        return move

    def accept_draw(self):
        # TODO
        print('TODO check if draw should be accepted.')
        return False

    #region tables
    pawntable = [
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10,-20,-20, 10, 10,  5,
    5, -5,-10,  0,  0,-10, -5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5,  5, 10, 25, 25, 10,  5,  5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0,  0,  0,  0,  0,  0,  0,  0]

    knightstable = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50]

    bishopstable = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -20,-10,-10,-10,-10,-10,-10,-20]

    rookstable = [
    0,  0,  0,  5,  5,  0,  0,  0,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    5, 10, 10, 10, 10, 10, 10,  5,
    0,  0,  0,  0,  0,  0,  0,  0]

    queenstable = [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  5,  5,  5,  5,  5,  0,-10,
    0,  0,  5,  5,  5,  5,  0, -5,
    -5,  0,  5,  5,  5,  5,  0, -5,
    -10,  0,  5,  5,  5,  5,  0,-10,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20]

    kingstable = [
    20, 30, 10,  0,  0, 10, 30, 20,
    20, 20,  0,  0,  0,  0, 20, 20,
    -10,-20,-20,-20,-20,-20,-20,-10,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30]



    centertable = [
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,10,10,10,10,0,0,
            0,0,10,25,25,10,0,0,
            0,0,10,25,25,10,0,0,
            0,0,10,10,10,10,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0]


    piecetypes = [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]
    tables = [pawntable, knightstable, bishopstable, rookstable, queenstable, kingstable]
    piecevalues = [100,320,330,500,900]

    #endregion

    def __init_evaluate_board(self, board):
        # p : pawn / n : knight / b : bishop / r : rock / q : queen 
        wp = len(board.pieces(chess.PAWN, chess.WHITE))
        bp = len(board.pieces(chess.PAWN, chess.BLACK))
        wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
        bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
        wb = len(board.pieces(chess.BISHOP, chess.WHITE))
        bb = len(board.pieces(chess.BISHOP, chess.BLACK))
        wr = len(board.pieces(chess.ROOK, chess.WHITE))
        br = len(board.pieces(chess.ROOK, chess.BLACK))
        wq = len(board.pieces(chess.QUEEN, chess.WHITE))
        bq = len(board.pieces(chess.QUEEN, chess.BLACK))

        material = 100*(wp-bp)+320*(wn-bn)+330*(wb-bb)+500*(wr-br)+900*(wq-bq)
    
        pawnsq = sum([self.pawntable[i] for i in board.pieces(chess.PAWN, chess.WHITE)])
        pawnsq= pawnsq + sum([-self.pawntable[chess.square_mirror(i)] 
                                        for i in board.pieces(chess.PAWN, chess.BLACK)])
        knightsq = sum([self.knightstable[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
        knightsq = knightsq + sum([-self.knightstable[chess.square_mirror(i)] 
                                        for i in board.pieces(chess.KNIGHT, chess.BLACK)])
        bishopsq= sum([self.bishopstable[i] for i in board.pieces(chess.BISHOP, chess.WHITE)])
        bishopsq= bishopsq + sum([-self.bishopstable[chess.square_mirror(i)] 
                                        for i in board.pieces(chess.BISHOP, chess.BLACK)])
        rooksq = sum([self.rookstable[i] for i in board.pieces(chess.ROOK, chess.WHITE)]) 
        rooksq = rooksq + sum([-self.rookstable[chess.square_mirror(i)] 
                                        for i in board.pieces(chess.ROOK, chess.BLACK)])
        queensq = sum([self.queenstable[i] for i in board.pieces(chess.QUEEN, chess.WHITE)]) 
        queensq = queensq + sum([-self.queenstable[chess.square_mirror(i)] 
                                        for i in board.pieces(chess.QUEEN, chess.BLACK)])
        kingsq = sum([self.kingstable[i] for i in board.pieces(chess.KING, chess.WHITE)]) 
        kingsq = kingsq + sum([-self.kingstable[chess.square_mirror(i)] 
                                        for i in board.pieces(chess.KING, chess.BLACK)])
        
        self.boardvalue = material + pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq

        return self.boardvalue


    def __update_eval(self, move,side):

        #update piecequares
        #move = chess.Move.from_uci(mov)
        movingpiece = self.board.piece_type_at(move.from_square)

        if side:
            self.boardvalue -= self.tables[movingpiece-1][move.from_square]

            #update for castle
            if (move.from_square == chess.E1) and (move.to_square == chess.G1):
                self.boardvalue -= self.rookstable[chess.H1]
                self.boardvalue += self.rookstable[chess.F1]
            
            elif (move.from_square == chess.E1) and (move.to_square == chess.C1):
                self.boardvalue -= self.rookstable[chess.A1]
                self.boardvalue += self.rookstable[chess.D1]

        else :
            self.boardvalue += self.tables[movingpiece - 1][move.from_square]
            
            #update for castle
            if (move.from_square == chess.E8) and (move.to_square == chess.G8):
                self.boardvalue -= self.rookstable[chess.H8]
                self.boardvalue += self.rookstable[chess.F8]
            
            elif (move.from_square == chess.E8) and (move.to_square == chess.C8):
                self.boardvalue -= self.rookstable[chess.A8]
                self.boardvalue += self.rookstable[chess.D8]


        if side:
            self.boardvalue += self.tables[movingpiece - 1][move.to_square]
        else:
            self.boardvalue -= self.tables[movingpiece - 1][move.to_square]
        
        #update material
        if move.drop != None:
            if side:
                self.boardvalue += self.piecevalues[move.drop-1]
            else:
                self.boardvalue -= self.piecevalues[move.drop-1]


        #update promotion
        if move.promotion != None:
            if side:
                self.boardvalue = self.boardvalue + self.piecevalues[move.promotion-1] - self.piecevalues[movingpiece-1]
                self.boardvalue = self.boardvalue - self.tables[movingpiece - 1][move.to_square] \
                    + self.tables[move.promotion - 1][move.to_square]
            else:
                self.boardvalue = self.boardvalue - self.piecevalues[move.promotion-1] + self.piecevalues[movingpiece-1]
                self.boardvalue = self.boardvalue + self.tables[movingpiece - 1][move.to_square] \
                    - self.tables[move.promotion -1][move.to_square]
                    
        return move

    def __minmax(self,board,depth, alpha,beta,turn):
        if depth == 0 or self.board.is_game_over():
            return self.__evaluate_board(self.board)

        if turn:
            best_move = -float('inf')
            for move in board.legal_moves:
                self.make_move(move)
                best_move = max(best_move,self.__minmax(board,depth-1,alpha,beta,not turn))
                self.unmake_move(board)
                alpha = max(alpha,best_move)
                if beta <= alpha:
                    return best_move
            return best_move
        else:
            best_move = float('inf')
            for move in board.legal_moves:
                self.make_move(move)
                best_move = min(best_move,self.__minmax(board,depth-1,alpha,beta,not turn))
                self.unmake_move(board)
                beta = min(beta,best_move)
                if beta <= alpha:
                    return best_move
            return best_move

    # simplified Evaluation 
    def __evaluate_board(self,board):
        
        if board.is_checkmate():
            if board.turn:
                return -9999
            else:
                return 9999
        

        if board.is_stalemate():
            return 0
        if board.is_insufficient_material():
            return 0
        # p : pawn / n : knight / b : bishop / r : rock / q : queen 
        wp = len(board.pieces(chess.PAWN, chess.WHITE))
        bp = len(board.pieces(chess.PAWN, chess.BLACK))
        wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
        bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
        wb = len(board.pieces(chess.BISHOP, chess.WHITE))
        bb = len(board.pieces(chess.BISHOP, chess.BLACK))
        wr = len(board.pieces(chess.ROOK, chess.WHITE))
        br = len(board.pieces(chess.ROOK, chess.BLACK))
        wq = len(board.pieces(chess.QUEEN, chess.WHITE))
        bq = len(board.pieces(chess.QUEEN, chess.BLACK))

        material = 100*(wp-bp)+320*(wn-bn)+330*(wb-bb)+500*(wr-br)+900*(wq-bq)

        pawnsq = sum([self.pawntable[i] for i in board.pieces(chess.PAWN, chess.WHITE)])
        pawnsq= pawnsq + sum([-self.pawntable[chess.square_mirror(i)] 
                                        for i in board.pieces(chess.PAWN, chess.BLACK)])
        knightsq = sum([self.knightstable[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
        knightsq = knightsq + sum([-self.knightstable[chess.square_mirror(i)] 
                                        for i in board.pieces(chess.KNIGHT, chess.BLACK)])
        bishopsq= sum([self.bishopstable[i] for i in board.pieces(chess.BISHOP, chess.WHITE)])
        bishopsq= bishopsq + sum([-self.bishopstable[chess.square_mirror(i)] 
                                        for i in board.pieces(chess.BISHOP, chess.BLACK)])
        rooksq = sum([self.rookstable[i] for i in board.pieces(chess.ROOK, chess.WHITE)]) 
        rooksq = rooksq + sum([-self.rookstable[chess.square_mirror(i)] 
                                        for i in board.pieces(chess.ROOK, chess.BLACK)])
        queensq = sum([self.queenstable[i] for i in board.pieces(chess.QUEEN, chess.WHITE)]) 
        queensq = queensq + sum([-self.queenstable[chess.square_mirror(i)] 
                                        for i in board.pieces(chess.QUEEN, chess.BLACK)])
        kingsq = sum([self.kingstable[i] for i in board.pieces(chess.KING, chess.WHITE)]) 
        kingsq = kingsq + sum([-self.kingstable[chess.square_mirror(i)] 
                                        for i in board.pieces(chess.KING, chess.BLACK)])
        
        boardvalue = material + pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq

        eval = boardvalue
        if board.turn:
            return eval
        else:
            return -eval