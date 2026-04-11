class Node:
    def __init__(self, val, left = None, right = None):
        self.val = val
        self.left = left
        self.right = right

""" For multiple queries

Time Complexity: O(nlogn) worst case, O(log n) amortied
    Preprocess: O(nlogn)
    1 query: O(log n)

Space Complexity:
"""

from collections import deque

def solve(root: Node, a: Node, b: Node):

    # Step 1: Find and set smaller depth (a, b)
    node_parent_map, node_depth_map = _bfs(root)

    if a not in node_depth_map or b not in node_depth_map:
        return None

    min_depth_node = a if node_depth_map[a] < node_depth_map[b] else b
    max_depth_node = b if min_depth_node == a else a

    # Step 2: Lift the deeper node  

    # Decompose the depth difference into powers of two
    # (e.g. 13 = 8 + 4 + 1)
    # -> if lca at depth 13 -> jump 1 -> 4 -> 8, instead of 1 -> 2 -> ... -> 13     
    up_table = _build_up_table(node_parent_map)
    
    depth_diff = node_depth_map[max_depth_node] - node_depth_map[min_depth_node]
    x = _lift(max_depth_node, depth_diff, up_table)
    y = min_depth_node

    if x == y: return x    

    # Step 3: Greedily move biggest -> smallest jump,
    # only jump if diff. parent (invariant)
    for k in range(len(up_table[x]) - 1, -1, -1):
        parent_x = up_table[x][k]; parent_y = up_table[y][k]
        if parent_x != parent_y:
            x = up_table[x][k]; y = up_table[y][k]

    return node_parent_map[x]

def _bfs(root):
    node_parent_map = {root: None}
    node_depth_map = {root: 0}
    
    q = deque([root])
    while q:
        
        node = q.popleft()
    
        for child in (node.left, node.right):
            if child is None: continue
            if child in node_parent_map: continue

            node_parent_map[child] = node
            node_depth_map[child] = node_depth_map[node] + 1
    
            q.append(child)

    return node_parent_map, node_depth_map

def _lift(node, depth_diff, up_table):
    k = 0  # k indexes the current 2^k (k = 0 -> 1 step, k = 1 -> 2 steps, ...)
    while depth_diff and node is not None:
        if (depth_diff & 1) == 1: # check if i'th bit == 1 (jump) or not
            node = up_table[node][k]

        # we move on from deciding about 2^k to deciding about 2^(k+1).
        depth_diff >>= 1
        k += 1

    return node

def _build_up_table(node_parent_map):
    """
    up[node][k] = 2^k-th parent of node, or -1 if doesn't exist.
	•	up[node][0] → parent (1 step)
	•	up[node][1] → grandparent (2 steps)
	•	up[node][2] → great-great-grandparent (4 steps)
	•	up[node][3] → 8 steps up

    Base case: up_table[node][0] = parents[node]
    Recurrence: up_table[node][k] = up_table[child][k-1] = up_table[up_table[node][k-1]][k-1]
    """
    n = len(node_parent_map)
    first_over_k = (n).bit_length() # first_over_k = first k where 2^k > n

    up_table = {node: [None for _ in range(first_over_k)] for node in node_parent_map}

    for node in node_parent_map:
        for k in range(first_over_k):
            ans = up_table[node][k]

            if k == 0:
                # Base case
                ans = node_parent_map[node]
            else:
                # 2^k = 2^{k-1} * 2 = 2^{k-1} + 2^{k-1}
                
                first_jump_node = up_table[node][k-1]  # First jump up by 2^{k-1} from node

                # Then jump up by another 2^{k-1} from mid
                ans = up_table[first_jump_node][k-1] if first_jump_node else None

            up_table[node][k] = ans
    
    return up_table