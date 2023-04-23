# Game-Tree-Search-

## Overview

In this assignment, you will implement search algorithms to solve several Checkers endgame puzzles, where a winning solution can always be found, given a strong enough AI.

The history of Checkers AI is a great story and a Canadian one! Check out the following article for the full tale: [How Checkers Was Solved](https://www.theatlantic.com/technology/archive/2017/07/marion-tinsley-checkers/534111/)

## Game Rules

Checkers is a two-player board game played on an eight by eight chess board. One player's pieces are black, and the other player's pieces are red. The players take turns moving pieces on the board. The red player moves first.
you can play checker through [this link](https://www.mathsisfun.com/games/checkers-2.html).

You can find the full rules at the link and also below

    Starting Position: Each player starts with 12 pieces on the dark squares of the three rows closest to that player's side. The black pieces start from the top three rows, and the red ones start from the bottom three. The red player makes the first move.
    Move Rules: There are two different ways to move.
        Simple move (see the left image in the figure above): A simple move involves moving a piece one square diagonally to an adjacent unoccupied dark square. Normal pieces can move diagonally forward only; kings can move in any diagonal direction. (For the black player, forward is down. For the red player, forward is up.)
        Jump (see the middle image in the figure above): A jump consists of moving a piece diagonally adjacent to an opponent's piece to an empty square immediately beyond it in the same direction (thus "jumping over" the opponent's piece front and back.) Normal pieces can jump diagonally forward only; kings can jump in any diagonal direction. A jumped piece is "captured" and removed from the game. Any piece, king or normal, can jump a king.
        Jumping is mandatory. If a player has the option to jump, they must make it, even if doing so results in a disadvantage for the jumping player. 
        Multiple jumps (see the right image in the figure above): After one jump, if the moved piece can jump another opponent's piece, it must keep jumping until no more jumps are possible, even if the jump is in a different diagonal direction. If more than one multi-jump is available, the player can choose which piece to jump with and which sequence of jumps to make. The sequence chosen is not required to be the one that maximizes the number of jumps in turn. However, a player must make all the available jumps in the sequence chosen.
    Kings:
        If a piece moves into the last row on the opponent's side of the board, it becomes a king and can move both forward and backward. A red piece becomes king when it reaches the top row, and a black piece becomes king when it reaches the bottom row. 
        If a piece becomes a king, the current move terminates; The piece cannot jump back as in a multi-jump until the next move.

    End of Game: A player wins by capturing all the opponent's pieces or when the opponent has no legal moves left.
    
## Task
implement a program that can solve a Checkers endgame puzzle using alpha-beta pruning and additional techniques of your choosing. 

program can be run through those command
   - python3 checkers.py --inputfile puzzle1.txt --outputfile puzzle1_sol.txt

## input and output format 
We will represent each state in the following format.
    Each state is a grid of 64 characters. The grid has eight rows with eight characters per row.
    ’.’ (the period character) denotes an empty square.
    ’r’ denotes a red piece,
    ’b’ denotes a black piece,
    ’R’ denotes a red king,
    ’B’ denotes a black king.

The following are the example of states
<pre>
```
........
....b...
.......R
..b.b...
...b...r
........
...r....
....B...
```
</pre>
Each input file contains one state. Your program controls the red pieces, and it is your turn to make a move.

Each output file contains the sequence of states until the end of the game. The first state is the same as the state in the input file. The last state is a state denoting the end of the game. There is one empty line between any two consecutive states.
The example of input and output are provided attached to README.md
[checkers2.txt](https://github.com/dkhhandsome/Game-Tree-Search-/files/11304819/checkers2.txt)
[solution2.txt](https://github.com/dkhhandsome/Game-Tree-Search-/files/11304820/solution2.txt)


