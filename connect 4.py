import numpy as np
import pygame
import sys
import math
ROW_COUNT=6
COL_COUNT=7
BLUE=(0,0,255)
BLACK=(0,0,0)
RED=(255,0,0)
YELLOW=(125,125,0)
WHITE=(255, 255, 255)
def create_board():#create matrix
    board=np.zeros((ROW_COUNT,COL_COUNT))
    return board
def drop_piece(board,row,col,piece):#will drop the piece
    board[row][col]=piece

def valid_location(board,col):#check col if last row is empty
    return board[ROW_COUNT-1][col]==0

def next_open_row(board,col):#loops to see the empty row to drop piece in it
    for r in range(ROW_COUNT):
        if board[r][col]==0:
            return r
def print_board(board):
    print(np.flip(board,0))
    
def wininng(board,piece):
    #check horizontal
    for c in range(COL_COUNT-3):#to be in index after adding the 3
        for r in range(ROW_COUNT):
            if board[r][c]==piece and board[r][c+1]==piece and board[r][c+2]==piece and board[r][c+3]==piece:
                return True
    #check vetical     
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c]==piece and board[r+1][c]==piece and board[r+2][c]==piece and board[r+3][c]==piece:
                return True            
            #check positivly slopped diagonlas
            
    for c in range(COL_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c]==piece and board[r+1][c+1]==piece and board[r+2][c+2]==piece and board[r+3][c+3]==piece:
                return True     
        #check negatively slopped diagonlas
    for c in range(COL_COUNT-3):
        for r in range(3,ROW_COUNT):
            if board[r][c]==piece and board[r-1][c+1]==piece and board[r-2][c+2]==piece and board[r-3][c+3]==piece:
                return True   
            
def full(board):#check if the map is full
    x=0
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c]!=0:
                x+=1
        if x==ROW_COUNT*COL_COUNT:
            return True    
def draw_board(board):#draw the game
    #rect(Surface, color, Rect)
    #circle(Surface, color, pos, radius)
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen,BLUE,(c*SQUARE_SIZE,r*SQUARE_SIZE+SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))
            if board[r][c]==0:#empty
                pygame.draw.circle(screen,BLACK,(int(c*SQUARE_SIZE+SQUARE_SIZE/2),int(r*SQUARE_SIZE+SQUARE_SIZE+SQUARE_SIZE/2)),RADIUS)
            elif board[r][c]==1:#player1
                pygame.draw.circle(screen,RED,(int(c*SQUARE_SIZE+SQUARE_SIZE/2),int(r*SQUARE_SIZE+SQUARE_SIZE+SQUARE_SIZE/2)),RADIUS)
            elif board[r][c]==2:#player2
                pygame.draw.circle(screen,YELLOW,(int(c*SQUARE_SIZE+SQUARE_SIZE/2),int(r*SQUARE_SIZE+SQUARE_SIZE+SQUARE_SIZE/2)),RADIUS)     
    pygame.display.update()
            

    
game_over= False
board=create_board()


turn=0
pygame.init()
SQUARE_SIZE=100 #square size
width=COL_COUNT*SQUARE_SIZE
height=(ROW_COUNT+2)*SQUARE_SIZE
size=(width,height)
screen = pygame.display.set_mode(size)

RADIUS=int(SQUARE_SIZE/2)
draw_board(board)
myfont=pygame.font.SysFont("monospace",50)


score1=0
score2=0
label=myfont.render("score:%d"%(score1),1,RED)
screen.blit(label,(SQUARE_SIZE*(COL_COUNT/10),(ROW_COUNT+1)*SQUARE_SIZE)) 
label=myfont.render("score:%d"%(score2),2,YELLOW)
screen.blit(label,(SQUARE_SIZE*(COL_COUNT/2),(ROW_COUNT+1)*SQUARE_SIZE)) 
#bot=1
pygame.display.update()
while not game_over:
    
    for event in pygame.event.get():#close button
        if event.type==pygame.QUIT:
            pygame.display.quit()
            sys.exit()
        
        label=myfont.render("score:%d"%(score1),1,RED)
        screen.blit(label,(SQUARE_SIZE*(COL_COUNT/10),(ROW_COUNT+1)*SQUARE_SIZE)) 
        label=myfont.render("score:%d"%(score2),2,YELLOW)
        screen.blit(label,(SQUARE_SIZE*(COL_COUNT/2),(ROW_COUNT+1)*SQUARE_SIZE))         
        if event.type==pygame.MOUSEMOTION:#draw the circle at the location of the mouse
            pygame.draw.rect(screen,BLACK,(0,0,width,SQUARE_SIZE))            
            posx=event.pos[0]
            
            if turn==0:#player1
                pygame.draw.circle(screen,RED,(posx,int(SQUARE_SIZE/2)),RADIUS) 
                
            else:#player2
                pygame.draw.circle(screen,YELLOW,(posx,int(SQUARE_SIZE/2)),RADIUS)  
                
        pygame.display.update()
        
        if event.type==pygame.MOUSEBUTTONDOWN: 
            pygame.draw.rect(screen,BLACK,(0,0,width,SQUARE_SIZE)) #to update the circle of the player           
            
            #player1
            if turn==0 :
                posx=event.pos[0]
                col=int(math.floor(posx/SQUARE_SIZE))#detrime the col
                if valid_location(board,col):#check if the col has a place
                    row = next_open_row(board,col)#findout the free row
                    drop_piece(board,row,col,1)#drop the piece in empty row
                    turn+=1
                    turn=turn%2                    
                    if wininng(board,1):#check if wininng
                        board=create_board()#check if won
                        pygame.draw.rect(screen,BLACK,(0,(ROW_COUNT+1)*SQUARE_SIZE,width,SQUARE_SIZE))
                        score1+=1
                        label=myfont.render("player 1 wins",1,RED)
                        screen.blit(label,(40,10))
                                            
            
            #player2
            else:
                posx=event.pos[0]
                col=int(math.floor(posx/SQUARE_SIZE))
                if valid_location(board,col):
                    row = next_open_row(board,col)
                    drop_piece(board,row,col,2)     
                    turn+=1
                    turn=turn%2                    
                    if wininng(board,2):
                        board=create_board()
                        pygame.draw.rect(screen,BLACK,(0,(ROW_COUNT+1)*SQUARE_SIZE,width,SQUARE_SIZE))
                        score2+=1
                        label=myfont.render("player 2 wins",2,YELLOW)
                        screen.blit(label,(40,10))
            #if bot==1:
                #board1=board.copy()
                #scores = {}
                #checkbestcol(board1,(turn+1),scores)
                #drop_best(board,scores)                    
            if full(board):
                label=myfont.render("full map will clean now",2,WHITE)
                screen.blit(label,(0,10))        
                board=create_board()
            pygame.display.update()
            draw_board(np.flip(board,0))
            




 #bot draft
#def scorec(board,piece):
    #scoreb=1
    ##check horizontal
    #for c in range(COL_COUNT-3):
        #for r in range(ROW_COUNT):
            #if board[r][c]==piece:
                #scoreb*=10
            #if board[r][c+1]==piece:
                #scoreb*=20
            #if board[r][c+2]==piece:
                #scoreb*=30
            #if board[r][c+3]==piece:
                #scoreb*=40
    ##check vetical 
    #for c in range(COL_COUNT):
        #for r in range(ROW_COUNT-3):
            #if board[r][c]==piece:
                #scoreb*=10
            #if board[r+1][c]==piece:
                #scoreb*=20
            #if board[r+2][c]==piece:
                #scoreb*=30
            #if board[r+3][c]==piece:
                #scoreb*=40
      ##check positivly slopped diagonlas
    #for c in range(COL_COUNT-3):
        #for r in range(ROW_COUNT-3):
            #if board[r][c]==piece:
                #scoreb*=10
            #if board[r+1][c+1]==piece:
                #scoreb*=20
            #if board[r+2][c+2]==piece:
                #scoreb*=30
            #if board[r+3][c+3]==piece:
                #scoreb*=40
    ##check negatively slopped diagonlas
    #for c in range(COL_COUNT-3):
        #for r in range(3,ROW_COUNT):
            #if board[r][c]==piece:
                #scoreb*=10
            #if board[r-1][c+1]==piece:
                #scoreb*=20
            #if board[r-2][c+2]==piece:
                #scoreb*=30
            #if board[r-3][c+3]==piece:
                #scoreb*=40                            
    #print(scoreb)
    #return scoreb
#def drop_pieceb(board1,row,col,piece):#will drop the piece
    #board1[row][col]=piece

#def fictionalmove(board1,piece,col,scores):
    #if valid_location(board1,col):
        #row = next_open_row(board1,col)
        #drop_piece(board1,row,col,1)
        #score=scorec(board1,1)
        #scores.update( {col : score} )
    
#def checkbestcol(board1,piece,scores):
    #for col in range(COL_COUNT):
        #board1=board.copy()
        #fictionalmove(board1,piece,col,scores)
#def drop_best(board,scores):
    #maximum = max(scores, key=scores.get)  # Just use 'min' instead of 'max' for minimum.
    ##print(maximum, scores[maximum])   
    ##drop_piece(board,row,maximum,1)  
    #col=maximum
    #if valid_location(board,col):
        #row = next_open_row(board,col)
        #drop_piece(board,row,col,1)
  