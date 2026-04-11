"""
Given two grids of same dimensions containing 0s and 1s,
count connected regions of 1s that are identical (same cells) in both grids.
"""

def solve(grid_a, grid_b):
    """ Time: O(n_row * n_col), n_row = len(grid_a), n_col = len(grid_a[0])
        Space: O(n_row * n_col)
    """
    return len(_find_components(grid_a) & _find_components(grid_b))


def _find_components(grid):
    """ BFS to extract all connected components as tuples of (r, c) in BFS order
        Time: O(n_row * n_col), n_row = len(grid), n_col = len(grid[0])
        Space: O(n_row * n_col)
    """
    from collections import deque
    n_row = len(grid)
    n_col = len(grid[0])

    visited_cells = set()
    components = set()
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for r in range(n_row):
        for c in range(n_col):
            if grid[r][c] == 0: continue
            if (r, c) in visited_cells: continue

            component_cells = []
            queue = deque([(r, c)])
            visited_cells.add((r, c))

            while queue:
                cur_r, cur_c = queue.popleft()
                component_cells.append((cur_r, cur_c))

                for dr, dc in dirs:
                    next_r = cur_r + dr
                    next_c = cur_c + dc

                    if not (0 <= next_r < n_row and 0 <= next_c < n_col): continue
                    if grid[next_r][next_c] == 0: continue
                    if (next_r, next_c) in visited_cells: continue

                    visited_cells.add((next_r, next_c))
                    queue.append((next_r, next_c))

            components.add(tuple(component_cells))

    return components


def test():
    grid_a = [
        [1, 1, 0, 0],
        [1, 0, 0, 1],
        [0, 0, 1, 1]
    ]
    grid_b = [
        [1, 1, 0, 1],
        [1, 0, 0, 0],
        [0, 0, 1, 1]
    ]
    # grid_a: {(0,0),(0,1),(1,0)} and {(1,3),(2,2),(2,3)}
    # grid_b: {(0,0),(0,1),(1,0)}, {(0,3)}, {(2,2),(2,3)}
    # Only {(0,0),(0,1),(1,0)} matches
    assert solve(grid_a, grid_b) == 1

    # Identical grids: all components match
    grid_c = [
        [1, 0],
        [0, 1]
    ]
    assert solve(grid_c, grid_c) == 2

    # No common components
    grid_d = [
        [1, 0],
        [0, 0]
    ]
    grid_e = [
        [0, 0],
        [0, 1]
    ]
    assert solve(grid_d, grid_e) == 0

    # All zeros
    grid_f = [
        [0, 0],
        [0, 0]
    ]
    assert solve(grid_f, grid_f) == 0

if __name__ == "__main__":
    test()