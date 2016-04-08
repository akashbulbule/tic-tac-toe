import numpy as np
import sys
import pygame
from pygame.locals import *
import easygui
import timeit


nextmov={}   #dictionary to change turns with alternate player
nextmov['X']='O'
nextmov['O']='X'
height = 50  #height of the square tile of tic tac toe
width = 50   #width of the square tile of tic tac toe
margin = 10  #margin between the square tiles in tic tac toe
total=0
def gameboard(n,board):   #draw the n*n square tiles for a n*n tic tac toe
	for row in range(n):
		for column in range(n):
			pygame.draw.rect(board,(255,255,255),[(width+margin)*column+margin,(margin+height)*row+margin,width,height])
	pygame.display.update()

def minmax1(k,mov,alpha,beta,depth,leveldepth,n):  #minmax algorithm with alpha beta pruning and 4-ply cuttoff with an evaluation function.
	global total
	j = evaluate1(k,leveldepth,mov,n)   #calculate if the node is a terminal node or if the depth is zero return the heuristic value
	if j[1] or depth==0:
		return (j[0],k,(0,0))

	r,c = np.where(k=='-')  #all possible positions available to play in terms of (r,c)
	score={}
	presentnode = k
	pos = (0,0)
	for i in range(len(r)):
		a=k.copy() 
		total+=1
		a[r[i]][c[i]]=mov #make the particular move and call minmax recursively to determine the heuristic value of the move
		levelscore = minmax1(a,nextmov[mov],alpha,beta,depth-1,leveldepth+1,n)
		if mov=='X':  #Computer's move
			if alpha<levelscore[0]: #MAX node
				alpha=levelscore[0]  #assign alpha to the max value of its children nodes and presentnode to that node which has the max value
				presentnode=a
				pos = (r[i],c[i])  #move played which maximises alpha


		else:
			if beta>levelscore[0]:  #MIN node
				beta=levelscore[0]  #assign beta to the min value of its children nodes and presentnode to that node which the min value
				presentnode=a
				pos = (r[i],c[i])  #move played which minimises alpha
		
		if beta<=alpha:
			break
	if mov=='X':
		return (alpha,presentnode,pos)
	else:
		return (beta,presentnode,pos)
		
def evaluate1(k,depth,mov,n): #evaluation function which calculates the number of only X's and only O's in a row,column and diagonal  
			X_line_occur = 0  #and returns the difference and the fact if the game is over(True) or not(False)
			O_line_occur = 0
			countoccur={}
			s1 = tuple(k.diagonal())  #return left diagonal 
			s2 = tuple(np.diag(np.fliplr(k))) #return right diagonal
			countoccur[s1] = (s1.count('X'),s1.count('O'))  #countoccurances of X and O 
			countoccur[s2] = (s2.count('X'),s2.count('O'))  # in both the diagonals
			if countoccur[s1][0]==n:
				return (sys.maxsize-depth,True)         #if all X's then return maxint-depth(win condition for max) else if all O's return 
			elif countoccur[s2][0]==n:					#-maxint+depth(win condition for min)
				return (sys.maxsize-depth,True)
			elif countoccur[s1][1]==n:
				return (-sys.maxsize+depth,True)
			elif countoccur[s2][1]==n:
				return (-sys.maxsize+depth,True)
			else:										#else add k*k to the heuristic value where k is no of X's and rest blank 
				if countoccur[s1][1]==0:
					X_line_occur += countoccur[s1][0]**2
				elif countoccur[s1][0]==0:
					O_line_occur += countoccur[s1][1]**2
				if countoccur[s2][1]==0:
					X_line_occur += countoccur[s2][0]**2
				elif countoccur[s2][0]==0:
					O_line_occur += countoccur[s2][1]**2

			for i in range(n):							#similarly calculate occurances of only X's and O's in rows and columns and return the difference
				s1 = tuple(k[:,i])
				s2 = tuple(k[i])
				countoccur={}
				countoccur[s1] = (s1.count('X'),s1.count('O'))
				countoccur[s2] = (s2.count('X'),s2.count('O'))
				if countoccur[s1][0]==n:
					return (sys.maxsize-depth,True)
				elif countoccur[s2][0]==n:
					return (sys.maxsize-depth,True)
				elif countoccur[s1][1]==n:
					return (-sys.maxsize+depth,True)
				elif countoccur[s2][1]==n:
					return (-sys.maxsize+depth,True)
				else:
					if countoccur[s1][1]==0:
						X_line_occur += countoccur[s1][0]**2
					elif countoccur[s1][0]==0:
						O_line_occur += countoccur[s1][1]**2
					if countoccur[s2][1]==0:
						X_line_occur += countoccur[s2][0]**2
					elif countoccur[s2][0]==0:
						O_line_occur += countoccur[s2][1]**2
			r,c = np.where(k=='-')  
			if mov=='X':
				if len(r)==0: #draw condition return heuristic value as 0 and since the game is over hence True as well.
					return (0,True)
				else:
					return ((X_line_occur-O_line_occur)-depth,False) #game isn't over return the difference and False
			else:
				if len(r)==0: 
					return (0,True)  #draw condition
				else:
					return ((O_line_occur-X_line_occur)+depth,False) #being the min player return the opposite of the max player value

					
def main():	
	global total
	n = raw_input("Enter the value of n:")  #enter the order of tic-tac-toe
	n = int(n)
	pygame.init() #set the gui for tic-tac-toe
	tictactoe = pygame.display.set_mode(((width+margin)*(n)+margin,(height+margin)*(n)+margin)) #screen size
	pygame.display.set_caption("Tic-Tac-Toe")  #caption of the display
	tictactoe.fill((0,0,0))  #background filled black
	font = pygame.font.Font(None, 100)  
	gameboard(n,tictactoe) #set the tiles for the game
	choice = easygui.boolbox("Do you want to play first?", title="New Game", choices=('Yes','No'))
	k = np.array([['-' for i in range(n)] for j in range(n)])  #initialize board configuration
	if choice==0: #if choice is 0 then max's turn else min's turn
		mov='X'
	else:
		mov='O'
	while True:
		if mov=='X':
			total=0
			f = minmax1(k,mov,-float('inf'),float('inf'),4,0,n) 
			k = f[1] #play the max move
			movcord = f[2] 
			print "the total nodes expanded by computer's present move:",total
			tictactoe.blit(font.render(mov, 1, (0,0,255)),((width+margin)*movcord[1]+margin,(height+margin)*movcord[0]+margin-5)) #display the move on the game screen
			pygame.display.update() #update the display screen
			mov = nextmov[mov] #change the move to O's move

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				return
			if event.type == pygame.MOUSEBUTTONDOWN: #detect the mouse button click by the user
				pos = pygame.mouse.get_pos()      #get the positions in pixels and convert to row,column coordinates
				r = (pos[0]-margin)/(width+margin)
				c = (pos[1]-margin)/(height+margin)
				o,p = np.where(k=='-')
				mv=[]
				for i in range(len(o)):
					mv+=[(o[i],p[i])]
				if (c,r) in mv:
					k[c][r]='O'
					tictactoe.blit(font.render(mov, 1, (255,0,0)),((width+margin)*r+margin-2,(height+margin)*c+margin-6)) #display user's move on screen
					pygame.display.update() #update the display
					mov = nextmov[mov]  #change the move to X's move
		j = evaluate1(k,0,'X',n)  #evaluate if the game is over or not
		win=0
		lost=0
		draw=0
		if j[1]:
			if j[0]>0: #computer(max's) win condition
				win = easygui.boolbox("Computer wins!!Do you want to restart the game?",title="Game Over",choices=('Yes','No'))
			elif j[0]<0:# player wins (min's) win condition
				lost = easygui.boolbox("You win!!Do you want to restart the game?",title = "Game Over",choices = ('Yes','No'))
			else:  #draw condition
				draw = easygui.boolbox("The game is a draw!!Do you want to restart the game?",title = "Game Over",choices = ('Yes','No'))
			if win or lost or draw: #if either of the above prompt to restart the game and reset the board configuration
				tictactoe.fill((0,0,0))
				gameboard(n,tictactoe)
				choice = easygui.boolbox("Do you want to play first?", title="New Game", choices=('Yes','No'))
				k = np.array([['-' for i in range(n)] for j in range(n)])
				if choice==0:
					mov='X'
				else:
					mov='O'
			else:
				pygame.quit()
				return				


if __name__ =="__main__":  #call main function
	main()	