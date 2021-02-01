import chess as chess
import chess.svg
import chess.polyglot
from chessboard import display
from IPython.display import SVG
import time


def init_evaluate_board(board):
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
    """
    pawnsq = sum([centertable[i] for i in board.pieces(chess.PAWN,chess.WHITE)])
    pawnsq = pawnsq + sum([-centertable[chess.square_mirror(i)]
       for i in board.pieces(chess.PAWN,chess.BLACK)])

    knightsq = sum([centertable[i]
       for i in board.pieces(chess.KNIGHT,chess.WHITE)])
    knightsq = knightsq + sum([-centertable[chess.square_mirror(i)]
       for i in board.pieces(chess.KNIGHT,chess.BLACK)])


    bishopsq = sum([centertable[i]
       for i in board.pieces(chess.BISHOP,chess.WHITE)])
    bishopsq = knightsq + sum([-centertable[chess.square_mirror(i)]
       for i in board.pieces(chess.BISHOP,chess.BLACK)])


    rooksq = sum([centertable[i]
       for i in board.pieces(chess.ROOK,chess.WHITE)])
    rooksq = knightsq + sum([-centertable[chess.square_mirror(i)]
       for i in board.pieces(chess.ROOK,chess.BLACK)])
    
    queensq = sum([centertable[i]
       for i in board.pieces(chess.QUEEN,chess.WHITE)])
    queensq = knightsq + sum([-centertable[chess.square_mirror(i)]
       for i in board.pieces(chess.QUEEN,chess.BLACK)])

    """ 
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


# simplified Evaluation 
def evaluate_board(board):
    
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

    eval = boardvalue
    if board.turn:
        return eval
    else:
        return -eval


# global structure for any pieces in the game // still simplified evaluation
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

checktable = [
        0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0]


def update_king(board):
    ki = 0
    for i in board.pieces(chess.KING, chess.WHITE):
        ki = i
    
  #  for j in checktable:



piecetypes = [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]
tables = [pawntable, knightstable, bishopstable, rookstable, queenstable, kingstable]
piecevalues = [100,320,330,500,900]

def update_eval(mov,side,board):
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

def make_mov(mov,board):
    update_eval(mov,board.turn,board)
    #m = chess.Move.from_uci("g1f3")
    board.push(mov)
    return mov

def unmake_move(board):
    mov = board.pop()
    update_eval(mov,not board.turn,board)
    
    return mov


def quiesce(alpha, beta,board):
    
    #stand_pat score : fail soft
    #beta fail hard

    stand_pat = evaluate_board(board)
    if(stand_pat >= beta):
        return beta
    if(alpha < stand_pat):
        alpha = stand_pat

    #until every_capture_has_been_examined
    for move in board.legal_moves:
        if board.is_capture(move):
            make_mov(move,board)
            score = -quiesce(-beta,-alpha,board)
            unmake_move(board)

            if(score >= beta):
                return beta
            if(score > alpha):
                alpha = score
    
    return alpha


def minmax(board,depth, alpha,beta,turn):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if turn:
        best_move = -float('inf')
        for move in board.legal_moves:
            make_mov(move,board)
            best_move = max(best_move,minmax(board,depth-1,alpha,beta,not turn))
            unmake_move(board)
            alpha = max(alpha,best_move)
            if beta <= alpha:
                return best_move
        return best_move
    else:
        best_move = float('inf')
        for move in board.legal_moves:
            make_mov(move,board)
            best_move = min(best_move,minmax(board,depth-1,alpha,beta,not turn))
            unmake_move(board)
            beta = min(beta,best_move)
            if beta <= alpha:
                return best_move
        return best_move

def alphaBetaMax(alpha, beta, depthleft,board):
    bestscore = -9999
    if(depthleft == 0):
        return quiesce(alpha,beta,board)

    for move in board.legal_moves:
        make_mov(move,board)
        score = -alphaBetaMax(-beta, -alpha, depthleft - 1,board)
        unmake_move(board)
        if score >= beta:
            return beta
        if score > bestscore:
            bestscore = score
        if score > alpha:
            alpha = score
    print(alpha)
    return bestscore




def selectmove(depth, board,turn):
        bestMove = chess.Move.null()
        bestValue = -float('inf')

        for move in board.legal_moves:
            make_mov(move,board)
            boardValue = minmax(board,depth-1,-float('inf'),float('inf'), not turn)
            unmake_move(board)
            if boardValue >= bestValue:
                bestValue = boardValue
                bestMove = move
        
        return bestMove



def playGameSelf(depth):
    board = chess.Board()
    print(board)
    print("Start :")
    print(board.is_game_over())
    boardvalue = init_evaluate_board(board)
    while(not board.is_game_over()):
        print("///////////////////")
        if board.turn:
            turn = True
        else:
            turn = False
        mov = selectmove(depth,board,turn)
        make_mov(mov,board)
        print(mov)
        print(board)
        time.sleep(0.5)


def playGame(depth):
    board = chess.Board()
    print(board)
    print("Start :")
    print(board.is_game_over())
    boardvalue = init_evaluate_board(board)
    while(not board.is_game_over()):
        print("///////////////////")
        if board.turn:
            turn = True
        else:
            turn = False
        mov = selectmove(depth,board,turn)
        make_mov(mov,board)
        print(mov)
        print(board)
        userMove = input("Enter valid chess move\n")
        print(userMove)
        board.push_san(userMove)
        print(board)
        #chess.svg.board(board,size=400,lastmove = mov)

playGame(3)
#chess.svg.board(board,size=400,lastmove = mov)
