"""
Sudoku Solver
LeetCode 37 - Difficulty: Hard

Write a program to solve a Sudoku puzzle by filling the empty cells.

A sudoku solution must satisfy all of the following rules:

• Each of the digits '1-9' must occur exactly once in each row.

• Each of the digits '1-9' must occur exactly once in each column.

• Each of the digits '1-9' must occur exactly once in each of the 9 '3x3' sub-boxes of the grid.

The ''.'' character indicates empty cells.



Constraints:

• 'board.length == 9'

• 'board[i].length == 9'

• 'board[i][j]' is a digit or ''.''.

• It is guaranteed that the input board has only one solution.
"""

def solve(board: list[list[str]]) -> None:
    n_row, n_col = len(board), len(board[0])
    FULL = (1 << 9) - 1  # digits 1..9

    row_mask_map = [0] * 9
    col_mask_map = [0] * 9
    zone_mask_map = [0] * 9        

    # init masks from board
    for r in range(n_row):
        for c in range(n_col):
            if board[r][c] != '.':
                zone = _rowCol_to_zone(r, c)
                bit = 1 << (ord(board[r][c]) - ord('1'))

                row_mask_map[r] |= bit
                col_mask_map[c] |= bit
                zone_mask_map[zone] |= bit

    def backtrack(pos, n_row, n_col):
        # jump to next empty
        while pos < n_row * n_col:
            r, c = _1d_to_2d(pos, n_col)
            if board[r][c] == '.':
                break
            pos += 1

        if pos == n_row * n_col:
            return True

        r, c = _1d_to_2d(pos, n_col)
        zone = _rowCol_to_zone(r, c)

        used = row_mask_map[r] | col_mask_map[c] | zone_mask_map[zone]
        avail = FULL & ~used

        while avail:
            bit = avail & -avail
            avail -= bit

            d = bit.bit_length() - 1
            val = chr(ord('1') + d)

            board[r][c] = val
            row_mask_map[r] |= bit
            col_mask_map[c] |= bit
            zone_mask_map[zone] |= bit

            if backtrack(pos + 1, n_row, n_col):
                return True

            row_mask_map[r] &= ~bit
            col_mask_map[c] &= ~bit
            zone_mask_map[zone] &= ~bit
            board[r][c] = '.'

        return False

    backtrack(0, n_row, n_col)

def _rowCol_to_zone(r, c):  # 9 x 9 -> 3 x 3
    return (r // 3) * 3 + (c // 3)  # zone id in [0..8]

def _1d_to_2d(pos, n_col):
    return (pos // n_col, pos % n_col)