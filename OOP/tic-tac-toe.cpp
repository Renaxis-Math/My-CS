"""
Design a Tic-tac-toe game that is played between two players on a n x n  grid.

You may assume the following rules:

A move is guaranteed to be valid and is placed on an empty block.
Once a winning condition is reached, no more moves is allowed.
A player who succeeds in placing n of their marks in a horizontal, vertical, or diagonal row wins the game.

Given _n_ = 3, assume that player 1 is "X" and player 2 is "O" in the board.

TicTacToe toe = new TicTacToe(3);

toe.move(0, 0, 1); - > Returns 0 (no one wins)
|X| | |
| | | |    // Player 1 makes a move at (0, 0).
| | | |

toe.move(0, 2, 2); -> Returns 0 (no one wins)
|X| |O|
| | | |    // Player 2 makes a move at (0, 2).
| | | |

toe.move(2, 2, 1); -> Returns 0 (no one wins)
|X| |O|
| | | |    // Player 1 makes a move at (2, 2).
| | |X|

toe.move(1, 1, 2); -> Returns 0 (no one wins)
|X| |O|
| |O| |    // Player 2 makes a move at (1, 1).
| | |X|

toe.move(2, 0, 1); -> Returns 0 (no one wins)
|X| |O|
| |O| |    // Player 1 makes a move at (2, 0).
|X| |X|

toe.move(1, 0, 2); -> Returns 0 (no one wins)
|X| |O|
|O|O| |    // Player 2 makes a move at (1, 0).
|X| |X|

toe.move(2, 1, 1); -> Returns 1 (player 1 wins)
|X| |O|
|O|O| |    // Player 1 makes a move at (2, 1).
|X|X|X|
"""

/* IDEA:

In Follow up, let's use a more efficient method. 
Then according to the prompts, 
we build a one-dimensional array of rows and cols with a size of n, 
as well as variable diagonal diag and inverse diagonal rev_diag. 

The idea of this method is that if player 1 puts a sub in a column 
in the first row, then rows[0] will increase by 1. 

If player 2 puts a sub in a column in the first row, 
then rows[0] will subtract 1. 

Then only when rows [0] is equal to n or -n, 
it means that the children in the first line are placed by a player, 
so the game can be returned to the player at the end of the end. 

Other rows and columns, diagonals and diagonals are all this idea. 
*/

class TicTacToe {
    public:
        /** Initialize your data structure here. */
        TicTacToe(int n): rows(n), cols(n), n(n), diag(0), rev_diag(0) {}
    
        int move(int row, int col, int player) {
            int add = player == 1 ? 1 : -1;

            rows[row] += add; 
            cols[col] += add;
            diag += (row == col ? add : 0);
            rev_diag += (row == n - col - 1 ? add : 0);

            return (
                // winning / losing condition
                abs(rows[row]) == n || abs(cols[col]) == n || 
                abs(diag) == n || abs(rev_diag) == n
            ) ? player : 0;
        }
    
    private:
        vector<int> rows, cols;
        int diag, rev_diag, n;
    };

