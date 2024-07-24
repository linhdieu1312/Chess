# initialize game state and find the valid move
class GameState():
    def __init__(self):
        # rook-R, knight-N, Bishop-B, pawn-p, Queen-Q, King-K
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"], 
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"], 
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]

        # add an dictionary to call the function move of each piece
        self.movePieceFunction = {
            'p' : self.getPawnMoves, 'R' : self.getRookMoves, 'N' : self.getKnightMoves, 
            'B' : self.getBishopMoves, 'Q' : self.getQueenMoves, 'K' : self.getKingMoves
        }

        self.whiteToMove = True
        self.moveLog = [] 
        # set the King location
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4)

        self.checkmate = False
        self.stalemate = False

    # take a move as 1 tham so va hoan thanh no
    def makeMove(self, move):
        if self.board[move.startRow][move.startCol] != "--":
            self.board[move.startRow][move.startCol] = "--"
            self.board[move.endRow][move.endCol] = move.pieceMoved
            # add move to movelog then we can undo it later or display the history of the game
            self.moveLog.append(move)
            # switch player turn: swap player
            self.whiteToMove = not self.whiteToMove

            # update the king location if moved
            if (move.pieceMoved == "wK"):
                self.whiteKingLocation = (move.endRow, move.endCol)
            elif (move.pieceMoved == "bK"):
                self.blackKingLocation = (move.endRow, move.endCol)
            
            if move.isPawnPromotion:
                self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

    # undo move: reverve all in makemove func
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            # update the king location if moved
            if (move.pieceMoved == "wK"):
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif (move.pieceMoved == "bK"):
                self.blackKingLocation = (move.startRow, move.startCol)

        self.checkmate = False
        self.stalemate = False

    def getValidMoves(self):
        moves = self.getAllPossibleMoves()
        
        for i in range(len(moves)-1, -1, -1):
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i]) # if the king be attacked, that is invalid move
            self.whiteToMove = not self.whiteToMove
            self.undoMove() 
            #  de dam bao so lan thay doi luot la so chan
            if len(moves) == 0:
                if self.inCheck():
                    self.checkmate = True
                else: 
                    self.stalemate = True
            else: 
                self.checkmate = False
                self.stalemate = False
        
        return moves
    
    # determine if the current player is in check
    def inCheck(self):
        if self.whiteToMove:
            return self.pieceUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else: 
            return self.pieceUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    # determine if the enemy can attack this piece
    def pieceUnderAttack(self, r, c):
        # switch to the opponent's turn
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()
        # switch turn back
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                # the piece under attack
                return True
        return False

    def getAllPossibleMoves(self):
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                # look at the board: the first letter : w, b, - show the turn
                turn = self.board[row][col][0] 
                
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    # consider each piece: pawn, rook, knight (bN, wN), bishop, king, queen
                    piece = self.board[row][col][1]
                    self.movePieceFunction[piece](row,col,moves)
        return moves

    # ---------- Get all the moves of each piece locate in (row, col )and add these to the list
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if self.board[r-1][c] == "--":
                moves.append(Move((r,c), (r-1,c), self.board))
                if r == 6 and self.board[r-2][c] == "--":
                    moves.append(Move((r,c), (r-2,c), self.board))
            # capture left
            if (c-1 >= 0):
                if self.board[r-1][c-1][0] == 'b': 
                    moves.append(Move((r,c), (r-1,c-1), self.board))
            # capture right
            if (c+1 <= 7):
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r,c), (r-1,c+1), self.board))

        # black pawn move
        else: 
            if self.board[r+1][c] == "--":
                moves.append(Move((r,c), (r+1,c), self.board))
                if r == 1 and self.board[r+2][c] == "--":
                    moves.append(Move((r,c), (r+2,c), self.board))
            if (c-1 >= 0):
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r,c), (r+1,c-1), self.board))
            if (c+1 <= 7):
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r,c), (r+1,c+1), self.board))

    def getRookMoves(self, r, c, moves):
        # directions is a tuple, in order of  up, , left, down, right
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1)) 
        enemyColor = 'b' if self.whiteToMove else 'w'

        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r,c), (endRow,endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r,c), (endRow,endCol), self.board))
                        break
                    else: 
                        break
                else:
                    break

    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1))
        #  allyColor: mau dong minh
        allyColor = 'w' if self.whiteToMove else 'b'
        # 
        for n in knightMoves:
            endRow = r + n[0]
            endCol = c + n[1]

            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                # neu ko phai dong minh
                if endPiece[0] != allyColor: 
                    moves.append(Move((r,c), (endRow,endCol), self.board))


    def getBishopMoves(self, r, c, moves):
        # directions is a tuple, in order 4 diaganols
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1)) 
        enemyColor = 'b' if self.whiteToMove else 'w'

        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r,c), (endRow,endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r,c), (endRow,endCol), self.board))
                        break
                    else: 
                        break
                else:
                    break

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1))
        allyColor = 'w' if self.whiteToMove else 'b'

        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                # neu ko phai dong minh
                if endPiece[0] != allyColor: 
                    moves.append(Move((r,c), (endRow,endCol), self.board))

    # ----------
class Move():
    # use dictionary map keys to values
    rankToRows = { "1" : 7, "2" : 6, "3" : 5, "4" : 4, "5" : 3, "6" : 2, "7" : 1, "8" : 0}
    rowToRanks = {v : k for k, v in rankToRows.items()}

    fileToCols = { "a" : 0, "b" : 1, "c" : 2, "d" : 3, "e" : 4, "f" : 5, "g" : 6, "h" : 7}
    colToFiles = {v : k for k, v in fileToCols.items()}

    def __init__(self, startPiece, endPiece, board):
        self.startRow = startPiece[0]
        self.startCol = startPiece[1]
        self.endRow = endPiece[0]
        self.endCol = endPiece[1]

        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

        # create moveID
        self.moveId = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol 

        self.isPawnPromotion = (self.pieceMoved == "wp" and self.endRow == 0) or (self.pieceMoved == "bp" and self.endRow == 7)

    # overriding method
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveId == other.moveId
        return False
        
    #function to return the rank file notation
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    #get the rank and file of 1 square: a1, col+row 
    def getRankFile(self, r, c):
        return self.colToFiles[c] + self.rowToRanks[r]