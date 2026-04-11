"""
Find the path with no repeating nodes and the maximum product of edge weights 
on a directed graph where all weights are greater than 0 AND < 1

Input (assume each node exists in keys): {
    node: [(child_node, w), ...],
    ...
}
"""

""" IDEA

1. Since w ∈ [0, 1), log(w) <= 0
-> maximizing sum(log(w)) = minimizing -sum(log(w)).
-> Dijkstra with edge weights -log(w) >= 0

2. Since no source defined, which is required for Dijkstra,
-> Dijkstra all sources if sparse graph (Floyd-Warshall if dense graph)

"""

def solve(node_neighborWeight_map):
    """ Implement Dijkstra for each node"""
    import math

    ans = float('inf')

    for node in node_neighborWeight_map:
        toNode_minDist_map = _dijkstra(
            node_neighborWeight_map, node,
            transform_weight_func = lambda w: -math.log(w)
        )

        for to_node, min_dist in toNode_minDist_map.items():
            if to_node != node:
                ans = min(ans, min_dist)
    
    return math.exp(-ans) if ans != float('inf') else 0

def _dijkstra(node_neighborWeight_map, src_node, *, transform_weight_func):

    """ Initially set all distances to max """
    toNode_minDist_map = {node: float('inf') for node in node_neighborWeight_map}

    """ Update distance for src node (since it' obvious) """
    toNode_minDist_map[src_node] = 0

    """ Init heap with the source node and its (true) answer """
    import heapq
    min_heap = [(toNode_minDist_map[src_node], src_node)] # (-log(w), node)

    """ while the heap """
    while min_heap:
        ele = heapq.heappop(min_heap)
        cum_dist, node = ele

        """ if even the best one so far is not optimal globall, discard"""
        if cum_dist > toNode_minDist_map[node]: continue

        for neighbor_node, weight in node_neighborWeight_map[node]:
            
            """ Update any cum. properties """
            new_cum_dist = cum_dist + transform_weight_func(weight)

            """ If we can reach neighbor node faster """
            if new_cum_dist < toNode_minDist_map[neighbor_node]:
                toNode_minDist_map[neighbor_node] = new_cum_dist
                heapq.heappush(min_heap, (new_cum_dist, neighbor_node))
    
    return toNode_minDist_map

""" Tests using edges (u, v, w) """
def test(edges):

    def _build_map(edges):
        ans = {}
        for node, child, w in edges:
            ans.setdefault(node, [])
            ans.setdefault(child, [])
            ans[node].append((child, w))
        return ans
    
    return round(solve(_build_map(edges)), 10)

# Single edge
assert test(edges = [(0, 1, 0.5)]) == 0.5

# Chain — best single hop among all pairs
assert test(edges = [(0, 1, 0.8), (1, 2, 0.5)]) == 0.8

# Bidirectional — picks the better direction
assert test(edges = [(0, 1, 0.3), (1, 0, 0.7)]) == 0.7

# Cycle — Dijkstra handles correctly without looping
assert test(edges = [(0, 1, 0.5), (1, 2, 0.6), (2, 0, 0.7)]) == 0.7

# Competing paths to same destination
assert test(edges = [(0, 1, 0.9), (1, 2, 0.9), (0, 2, 0.5)]) == 0.9

# General Test
edges = [
    (0, 1, 0.9), (0, 2, 0.7),
    (1, 3, 0.8), (2, 3, 0.6),
    (1, 4, 0.5), (4, 5, 0.3),
    (3, 5, 0.4)
]
assert test(edges) == 0.9