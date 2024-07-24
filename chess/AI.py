import random
from typing import Counter

# dictionary
pieceScore = {"K" : 0, "Q" : 10, "R" : 5, "B" : 3, "N" : 3, "p" : 1}
# GTRI AM: BALCK WINS, GTRI DUONG: WHITE WINS
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3

def RandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]

def bestMove(gs, validMoves):
    global nextMove, counter
    nextMove = None
    random.shuffle(validMoves)
    counter = 0
    # minimax(gs, validMoves, DEPTH, gs.whiteToMove)
    # negamaxalphabeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    negamax(gs, validMoves, DEPTH, 1 if gs.whiteToMove else -1)
    # minimaxalphabeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, gs.whiteToMove)
    print("----------------")
    print("AI is thinking..")
    print(counter)
    return nextMove

# minimax
def minimax(gs, validMoves, depth, whiteToMove):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return evaluation(gs)
    
    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = minimax(gs, nextMoves, depth-1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move    
            gs.undoMove()
        return maxScore  
    
    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = minimax(gs, nextMoves, depth-1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move    
            gs.undoMove()
        return minScore  
# minimax alpha beta
def minimaxalphabeta(gs, validMoves, depth, alpha, beta, whiteToMove):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return evaluation(gs)
    
    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = minimaxalphabeta(gs, nextMoves, depth-1, alpha, beta, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move    
            gs.undoMove()
            if maxScore > alpha:
                alpha = maxScore
            if alpha >= beta:
                break
        return maxScore  
    
    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = minimaxalphabeta(gs, nextMoves, depth-1, alpha, beta, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move    
            gs.undoMove()
            if minScore < beta:
                beta = minScore
            if alpha >= beta:
                break
        return minScore  

# negamax
def negamax(gs, validMoves, depth, turn):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turn * evaluation(gs)
    
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = negamax(gs, nextMoves, depth-1, -turn)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move    
        gs.undoMove()
    return maxScore      
    

# negamax alpha beta
def negamaxalphabeta(gs, validMoves, depth, alpha, beta, turn):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turn * evaluation(gs)
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -negamaxalphabeta(gs, nextMoves, depth-1, -beta, -alpha, -turn)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move   
        gs.undoMove()
        # prunning after this
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore       

def evaluation(gs):
    if gs.checkmate:
        if gs.whiteToMove:
            # black wins
            return -CHECKMATE 
        else:
            # white wins
            return CHECKMATE
    elif gs.stalemate:
        return STALEMATE
    
    score = 0
    for row in gs.board:
        for piece in row:
            if piece[0] == "w":
                score += pieceScore[piece[1]]
            elif piece[0] == "b":
                score -= pieceScore[piece[1]]
    return score
        

