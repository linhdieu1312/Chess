from os import pipe
import pygame as pg
from pygame import Color
from pygame.constants import KEYDOWN, QUIT
# tu folder chess chen file engine vao
import engine 
import AI

WIDTH = HEIGHT = 512
DIMESION = 8
SQ_SIZE = HEIGHT // DIMESION
MAX_FPS = 15
IMAGES = {}

Move_Panel_Height = 512
Move_Panel_Width = 200
def loadImg():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bp", "wR", "wN", "wB", "wK", "wQ", "wp"]
    for piece in pieces:
        # load images from folder images
        img = pg.image.load("images/"+ piece +".png")
        # set the size
        IMAGES[piece] = pg.transform.scale(img, (SQ_SIZE, SQ_SIZE))


# main: handle user input and update graphic
def main():
    pg.init()
    screen = pg.display.set_mode((WIDTH+Move_Panel_Width, HEIGHT))
    pg.display.set_caption("Chess AI")
    screen.fill(pg.Color("white"))

    # create obj game state 
    gs = engine.GameState()

    validMoves = gs.getValidMoves() 
    moveMade = False

    loadImg() 
    running = True
    # use an empty tuple to keep track the last click of user
    pieceSelected = ()
    # keep track player clicks [(), ()] list :add 2 tuples
    playerClicks = [] 

    gameOver = False

    # AI
    # if a human play white then playerOne =True, then AI is playing, it is False
    playerOne = False
    playerTwo = True  # it is black turn
    
    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False

            # mouse handlers

            elif e.type == pg.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    # get (x,y) location of mouse, location is a list 
                    location = pg.mouse.get_pos() 
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    # if user click in their own location then 
                    if pieceSelected == (row, col) or col >= 8:
                        pieceSelected = ()
                        playerClicks = []
                    else: 
                        pieceSelected = (row, col)
                        # append both 1st click and 2nd click
                        playerClicks.append(pieceSelected)
                    if len(playerClicks) == 2:
                        # creat an object of move class: move(self, startPiece, endPiece, board):
                        move = engine.Move(playerClicks[0], playerClicks[1], gs.board) 
                        print("----------------")
                        print("Your turn!")
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                            # reset user click and playerclick then it can be 2 (if not, playerClick continously increase then no longer equal 2)
                                pieceSelected = ()
                                playerClicks = []
                        if not moveMade:
                            # save current click la click t2 neu chon lai cay co muon di
                            playerClicks = [pieceSelected]
                    
            # key handlers
            elif e.type == pg.KEYDOWN: 
                if e.key == pg.K_z:
                    gs.undoMove()  
                    moveMade = True
                    gameOver = False

        # AI move
        if not gameOver and not humanTurn:
            pg.display.set_caption("AI is thinking....")
            AImove = AI.bestMove(gs, validMoves)
            if AImove is None:
                AImove = AI.RandomMove(validMoves)
            gs.makeMove(AImove)
            print(AImove.getChessNotation())
            moveMade = True
            pg.display.set_caption("Chess AI")


        if moveMade:
            # need to get new valid move
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs, validMoves, pieceSelected)

        if gs.checkmate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, 'Black wins by checkmate')
            else:
                drawText(screen, 'White wins by checkmate')
        elif gs.stalemate:
            gameOver = True
            drawText(screen, 'Stalemate')
        pg.display.flip()

# highlight the square selected and move for the selected piece
def highlightSquare(screen, gs, validMoves, pieceSelected):
    if pieceSelected != ():
        r, c = pieceSelected
        if gs.board[r][c][0] == ("w" if gs.whiteToMove else "b"):
            # highlight the selected piece
            s = pg.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(pg.Color("blue"))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE)) 

            # highlight the valid move from that piece
            s.fill(pg.Color("yellow"))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (SQ_SIZE*move.endCol, SQ_SIZE*move.endRow))

# draw game state:
def drawGameState(screen, gs, validMoves, pieceSelected):
    drawBoard(screen)
    drawPieces(screen, gs.board)
    highlightSquare(screen, gs, validMoves, pieceSelected)
    drawMoveLog(screen, gs)


# draw square on board, top left is always white mean (0.0) = white
def drawBoard(screen):
    # colors list has color[0] = white (mean light square), color[1] = dark square
    colors = [pg.Color("white"), pg.Color("light gray")] 
    # range(a): take number from 0 -> a-1
    for row in range(DIMESION): 
        for col in range(DIMESION):
            # %2 chia lay du
            color = colors[((col+row)%2)] 
            pg.draw.rect(screen, color, pg.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))

# draw pieces on board base on the current game state 's board
def drawPieces(screen, board):
    for row in range(DIMESION): 
        for col in range(DIMESION):
            piece = board[row][col]
            if piece != "--":
                screen.blit(IMAGES[piece], pg.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawMoveLog(screen, gs):
    font = pg.font.SysFont("Arial", 16, True, False)
    moveLogRect = pg.Rect(HEIGHT, 0, Move_Panel_Width, Move_Panel_Height)
    pg.draw.rect(screen, pg.Color("light blue"), moveLogRect)
    moveLog = gs.moveLog
    moveLogText = moveLog
    padding = 5
    spacing = 5
    for i in range(len(moveLogText)):
        text = moveLogText[i].getChessNotation()
        textObj = font.render(text, True, pg.Color("White"))
        textPos = moveLogRect.move(padding, spacing)
        screen.blit(textObj, textPos)
        spacing += textObj.get_height()


def drawText(screen, text):
    font = pg.font.SysFont("Helvitca", 32, True, False)
    textObj = font.render(text, 0, pg.Color("Gray"))
    textPos = pg.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObj.get_width()/2, HEIGHT/2 - textObj.get_height()/2)
    screen.blit(textObj, textPos)
    textObj = font.render(text, 0, pg.Color("Red"))
    screen.blit(textObj, textPos.move(2,2))
    

if __name__ == "__main__":
    main()