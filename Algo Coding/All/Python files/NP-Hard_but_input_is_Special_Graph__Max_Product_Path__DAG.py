"""
Find the path with no repeating nodes and the maximum product of edge weights 
on a directed complete acyclic graph where all weights are greater than 0

Input (assume each node exists in keys): {
    node: [(child_node, w), ...],
    ...
}
"""

""" IDEA

max product(w) = max sum of log(w)
"""

def solve(node_neighborWeight_map) -> tuple[list, int]: # optimal path, product
    import math

    if not node_neighborWeight_map: return [], 0

    # get topo order first
    node_indegree_map = {node: 0 for node in node_neighborWeight_map}
    for node in node_neighborWeight_map:
        for child_node, _ in node_neighborWeight_map[node]:
            node_indegree_map.setdefault(child_node, 0)
            node_indegree_map[child_node] += 1
    roots = [node for node in node_indegree_map if node_indegree_map[node] == 0]

    topo_nodes = _get_topo_nodes(node_neighborWeight_map, node_indegree_map, roots)

    # answers[i] = ans ending at node i
    # base case = None node = log(1) = 0.0
    answers = {node: 0.0 for node in node_indegree_map}

    # record optimal path via node_parent_map
    node_parent_map = {node: None for node in node_indegree_map}

    for node in topo_nodes:
        for child_node, w in node_neighborWeight_map.get(node, []):
            candidate_ans = answers[node] + math.log(w)

            if candidate_ans > answers[child_node]:
                answers[child_node] = candidate_ans

                # record
                node_parent_map[child_node] = node

    # Get the optimal path and product
    best_leaf_node = max(answers.keys(), key = lambda x: answers[x])
    path = _reconstruct(node_parent_map, best_leaf_node)

    # Get optimal product
    node_neighbor_weight_map = {
        node: dict(node_neighborWeight_map[node])
        for node in node_neighborWeight_map
    }
    ans = 1
    for i in range(1, len(path)):
        node, child = path[i-1], path[i]
        ans *= node_neighbor_weight_map[node][child]

    return path, ans
    
def _get_topo_nodes(node_neigbors_map, node_indegree_map, roots):
    from collections import deque

    answers = []

    queue = deque(roots)
    while queue:
        node = queue.popleft()
        answers.append(node)

        for child_node, _ in node_neigbors_map.get(node, []):
            node_indegree_map[child_node] -= 1
            if node_indegree_map[child_node] == 0:
                queue.append(child_node)

    return answers

def _reconstruct(node_parent_map, start_node) -> list:
    answers = []

    node = start_node
    while node is not None:
        answers.append(node)
        node = node_parent_map[node]
    
    answers.reverse()
    return answers

""" Tests using edges (u, v, w) """
def test(edges):

    def _build_map(edges):
        ans = {}
        for node, child, w in edges:
            ans.setdefault(node, [])
            ans[node].append([child, w])
        return ans
    
    return solve(_build_map(edges))

# Linked List DAG
assert test(edges = [(0, 1, 2), (1, 2, 3)]) == ([0, 1, 2], 6)

# Balanced Tree
assert test(edges = [(0, 1, 2), (0, 2, 10)]) == ([0, 2], 10)

# Longer Branch beat Shorter
assert test(edges = [(0, 1, 2), (1, 2, 2), (0, 2, 3)]) == ([0, 1, 2], 4)

# General Test
edges = [
    (0, 1, 2), (0, 2, 3),
    (1, 3, 5), (2, 3, 2),
    (1, 4, 2), (4, 5, 10),
    (3, 5, 2)
]
assert test(edges) == ([0, 1, 4, 5], 40)