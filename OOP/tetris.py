# STEP 1
SHAPES = {
    'I': ((0, 0), (-1, 0), (1, 0), (2, 0)),
    'O': ((0, 0), (1, 0), (0, 1), (1, 1)),
    'S': ((0, 0), (0, -1), (-1, 0), (-1, 1)),
    'Z': ((0, 0), (-1, -1), (-1, 0), (0, 1)),
    'T': ((0, 0), (0, -1), (0, 1), (1, 0)),
    'L': ((0, 0), (0, -1), (0, 1), (1, 1)),
    'J': ((0, 0), (0, -1), (0, 1), (1, -1))
}

MOVES = {
    'a': (0, -1),   # left
    's': (1, 0),    # down
    'd': (0, 1),    # right
    'r': 'rotate',
    'q': 'quit'
}

# Cell State
from enum import Enum
class Cell(Enum):
    EMPTY = ' '      # Empty cell
    ACTIVE = '#'     # Active piece (temporary, player can move, can destroy other pieces)
    LOCKED = 'x'     # Locked piece (permanent part of board)
# END STEP 1

import os
import random

# STEP 2
class Grid:

    def __init__(self, width, height):
        self.w = width
        self.h = height
        self.grid = self._init_grid(self.w, self.h)
        self.active_piece = Piece(self.w) # the piece user can move

    def _init_grid(self, w, h):
        return [[Cell.EMPTY.value for _ in range(w)] for _ in range(h)]

    def __repr__(self) -> str:
        # clear screen
        os.system('clear')

        grid_copy = [row[:] for row in self.grid]

        # Print the active piece
        for r, c in self.active_piece.coords:
            if 0 <= r < self.h and 0 <= c < self.w:
                grid_copy[r][c] = Cell.ACTIVE.value

        # Formatting rows
        rows = ['|' + ''.join(row) + '|' for row in grid_copy]
        border = ' ' + '-' * (self.w) + ' '

        return '\n'.join([*rows, border])

# END STEP 2

# STEP 6
    def update(self, player_move) -> bool:
        if not player_move: raise ValueError

        # Try user move (rotate or left/right/down)
        new_piece = self.active_piece.move(player_move)
        if self._can_move(new_piece): self.active_piece = new_piece
        
        # Always apply 'drop by 1' after player move ends
        final_piece = self.active_piece.move('s')  # 's' is the key for down
        
        if self._can_move(final_piece):
            self.active_piece = final_piece
            return True

        elif self._can_destroy_pieces():
            return True
        
        else: return False

    def _can_move(self, piece) -> bool:

        def _fit(r, c):
            in_bounds_col = 0 <= c < self.w
            within_height = r < self.h

            if not (in_bounds_col and within_height):
                return False

            if r < 0: return True

            return self.grid[r][c] == Cell.EMPTY.value

        return all(_fit(r, c) for r, c in piece.coords)        

    def _can_destroy_pieces(self) -> bool:
        self._lock_piece()
        self._destroy()
        # Can update score here

        self.active_piece = Piece(self.w)           # Generate a random new piece
        return self._can_move(self.active_piece)    # Check if game over

    def _lock_piece(self):
        for r, c in self.active_piece.coords:
            if r >= 0:  # not hit pass the ceiling
                self.grid[r][c] = Cell.LOCKED.value   

    def _destroy(self):
        # Keep rows that are NOT completely filled with locked pieces
        incomplete_rows = [
            row for row in self.grid
            if not all(cell == Cell.LOCKED.value for cell in row)
        ]

        empty_row_count = self.h - len(incomplete_rows)        
        if empty_row_count:
            self.grid = self._init_grid(self.w, empty_row_count) + incomplete_rows
# END STEP 6

# STEP 3
class Piece():

    def __init__(self, grid_w = None, coords = []):
        self.coords = coords if coords else self._randomize(grid_w)

    @staticmethod
    def _randomize(grid_width):
        desired_shape = random.choice(list(SHAPES))
        shape_coords = SHAPES[desired_shape]

        cols = [c for _, c in shape_coords]
        min_col = min(cols)
        max_col = max(cols)

        left_bound = -min_col
        right_bound = grid_width - 1 - max_col

        if right_bound < left_bound:
            raise ValueError("Grid width is too small for the Tetris pieces.")

        random_col = random.randint(left_bound, right_bound)
        return [
            [r, c + random_col]
            for r, c in shape_coords
        ]

    def move(self, dir):
        if dir == 'r': return self._rotate()  # 'r' is the key, 'rotate' is the value
        
        dr, dc = MOVES[dir]
        return Piece(coords = [[r + dr, c + dc] for r, c in self.coords])

    def _rotate(self):
        pivot_r, pivot_c = self.coords[0]
        rotated_coords = [
            [pivot_r + (c - pivot_c), pivot_c - (r - pivot_r)] 
            for r, c in self.coords
        ]
        return Piece(coords = rotated_coords)
# END STEP 3

# STEP 4
class Player:

    def __init__(self):
        self.input_width = self._parse_input(input('Width: '))
        self.input_height = self._parse_input(input('Height: '))
        self.history = []

    def _parse_input(self, user_input) -> int:
        while not user_input.isnumeric():
            user_input = input("Invalid input. Please re-enter: ")
        return int(user_input)

    def get_move(self) -> str:
        player_move = self._parse_move(input(f"Select a move ({list(MOVES)}): ").strip().lower())
        self.history.append(player_move)
        return player_move  # Return the key, not the value, so move() can look it up

    def _parse_move(self, user_input) -> str:
        while not user_input in MOVES:
            user_input = input("Invalid input. Please re-enter: ")
        return user_input        
# END STEP 4

# STEP 5
class Game:
    def __init__(self):
        self.player = Player()
        self.Grid = Grid(self.player.input_width, self.player.input_height)
        self.is_game_over = False

    def run(self):
        while not self.is_game_over:
            print(self.Grid)

            player_move = self.player.get_move()
            if player_move == 'q':  # 'q' is the key, 'quit' is the value
                self.is_game_over = True
                continue

            sucess = self.Grid.update(player_move)

            # Update
            self.is_game_over = not sucess
# END STEP 5

if __name__ == "__main__":
    game = Game()
    game.run()