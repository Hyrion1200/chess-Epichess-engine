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
        self.turn += 1

    def get_move(self):
        print('TODO get move')
        return "e2e4"

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
        global boardvalue
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
    
        pawnsq = sum([pawntable[i] for i in board.pieces(chess.PAWN, chess.WHITE)])
        pawnsq= pawnsq + sum([-pawntable[chess.square_mirror(i)] 
                                        for i in board.pieces(chess.PAWN, chess.BLACK)])
        knightsq = sum([knightstable[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
        knightsq = knightsq + sum([-knightstable[chess.square_mirror(i)] 
                                        for i in board.pieces(chess.KNIGHT, chess.BLACK)])
        bishopsq= sum([bishopstable[i] for i in board.pieces(chess.BISHOP, chess.WHITE)])
        bishopsq= bishopsq + sum([-bishopstable[chess.square_mirror(i)] 
                                        for i in board.pieces(chess.BISHOP, chess.BLACK)])
        rooksq = sum([rookstable[i] for i in board.pieces(chess.ROOK, chess.WHITE)]) 
        rooksq = rooksq + sum([-rookstable[chess.square_mirror(i)] 
                                        for i in board.pieces(chess.ROOK, chess.BLACK)])
        queensq = sum([queenstable[i] for i in board.pieces(chess.QUEEN, chess.WHITE)]) 
        queensq = queensq + sum([-queenstable[chess.square_mirror(i)] 
                                        for i in board.pieces(chess.QUEEN, chess.BLACK)])
        kingsq = sum([kingstable[i] for i in board.pieces(chess.KING, chess.WHITE)]) 
        kingsq = kingsq + sum([-kingstable[chess.square_mirror(i)] 
                                        for i in board.pieces(chess.KING, chess.BLACK)])
        
        boardvalue = material + pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq

        return boardvalue


    def __update_eval(self, mov,side,board):
        global boardvalue

        #update piecequares
        movingpiece = board.piece_type_at(mov.from_square)

        if side:
            boardvalue -= tables[movingpiece-1][mov.from_square]

            #update for castle
            if (mov.from_square == chess.E1) and (mov.to_square == chess.G1):
                boardvalue -= rookstable[chess.H1]
                boardvalue += rookstable[chess.F1]
            
            elif (mov.from_square == chess.E1) and (mov.to_square == chess.C1):
                boardvalue -= rookstable[chess.A1]
                boardvalue += rookstable[chess.D1]

        else :
            boardvalue += tables[movingpiece - 1][mov.from_square]
            
            #update for castle
            if (mov.from_square == chess.E8) and (mov.to_square == chess.G8):
                boardvalue -= rookstable[chess.H8]
                boardvalue += rookstable[chess.F8]
            
            elif (mov.from_square == chess.E8) and (mov.to_square == chess.C8):
                boardvalue -= rookstable[chess.A8]
                boardvalue += rookstable[chess.D8]


        if side:
            boardvalue += tables[movingpiece - 1][mov.to_square]
        else:
            boardvalue -= tables[movingpiece - 1][mov.to_square]
        
        #update material
        if mov.drop != None:
            if side:
                boardvalue += piecevalues[mov.drop-1]
            else:
                boardvalue -= piecevalues[mov.drop-1]


        #update promotion
        if mov.promotion != None:
            if side:
                boardvalue = boardvalue + piecevalues[mov.promotion-1] - piecevalues[movingpiece-1]
                boardvalue = boardvalue - tables[movingpiece - 1][mov.to_square] \
                    + tables[mov.promotion - 1][mov.to_square]
            else:
                boardvalue = boardvalue - piecevalues[mov.promotion-1] + piecevalues[movingpiece-1]
                boardvalue = boardvalue + tables[movingpiece - 1][mov.to_square] \
                    - tables[mov.promotion -1][mov.to_square]
                    
        return mov
