#**N*N Tic Tac Toe using Minmax with alpha-beta pruning**


##**Introduction:**

We have implemented a tic tac toe game where a human user user can play
the game with a computer. Tic tac toe is a two player game where a
player can either choose Noughts(‘O’) or crosses(‘X’) as his move. The
two players take turns marking the spaces in a nxn grid. The player who
succeeds in placing three respective marks in a horizontal, vertical, or
diagonal row wins the game. If each player makes his best moves the game
can result in a draw.


##**Objective:**

The objective of this project was to develop a tic tac toe game where
the user can interactively play with the computer. In the beginning of
game the user is asked to choose the size of the board he wants to play
in. Once he enters a number he is provided with a choice whether he
wants to play the first move or not. Thereafter the game begins.

##**Algorithm:**


####**Minimax:**

The game is built on minimax algorithm. The idea of this algorithm is
based on a back and forth between the two participating players. One of
the players always desires to make a move with the maximum score. The
opposing player in turn decides which of its available moves has the
minimum score and chooses it. In the next step the maximizing player
again tries to maximize its score among its available moves. This
continues all the way down the game tree till it reaches an end state.
In our case we have chosen the computer ( X player ) as the one trying
to maximizing the score while the user (O player ) as the one trying to
minimize the score.


####**Evaluation Function:**

To determine whether a certain board position is ‘good’ or ‘bad’ for a
certain player we use an evaluation function. The function enables the
algorithm to look ahead and determine the kind of moves it can actually
make.

1.  If there are n X’s and no O’s in a row, column or diagonal then we
    return infinity.

2.  If there are n O’s and no X’s in a row, column or diagonal then we
    return -infinity.

3.  If there are k X’s for 0&lt;k&lt;n and no O’s in a row, column or
    diagonal return k^2^ for each such instance.

4.  If there are k O’s for 0&lt;k&lt;n and no X’s in a row, column or
    diagonal return -k^2^ for each such instance.


####**Alpha Beta Pruning:**

This is an optimization technique which helped saved us a lot of
searching and increasing our maximal search depth. It stops completely
evaluating a move when at least one possibility has been found that
proves the move to be worse than a previously examined move. We have
alpha and beta as two variables for each node we are analyzing. Alpha
will be the value of the best possible move the computer can make, that
have been computed so far. Beta will be the value of the best possible
move the user can make, that have been computed so far. If at any time,
alpha &gt;= beta, then the user's best move can force a worse position
than computer’s best move so far, and so there is no need to further
evaluate this move. Initially alpha has the value –infinity and beta has
the value –infinity and we gradually update the values as we move on.

####**Minimax Cut off:**

We have set the searching depth to be at 4.


##**Language:**

This project has been developed using Python 2.7.3. We use two external
packages pygame and easygui for the implementation of the graphical user
interface.


##**How to run the program?**

1.  Install python 2.7.3 and the external packages ‘pygame’ and
    ‘easygui’

2.  Type python FinalProj.py in the command prompt.

##**Future Improvements:**

A possible future improvement can be increasing the depth cutoff from 4
to a higher value. We have to take care the algorithm is optimized
enough to handle such a large number of nodes.
