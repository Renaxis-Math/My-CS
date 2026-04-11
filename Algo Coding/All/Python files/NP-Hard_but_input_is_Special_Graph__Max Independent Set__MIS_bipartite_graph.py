"""
Same problem as MIS_tree.py but input is a bipartite graph instead of a tree.

Given a graph of "i hate you" between people
ensuring the resulting graph is an undirected, connected bipartite graph,
what is the maximum number of people I can select s.t no one hates each other?

Input (assumes all nodes exists as keys): 
{
    <node> : [<hate_node>, ...],
    ...
}
"""

""" IDEA: König's theorem

"max people we can pick" = total people - "max pairs we can match"

Hopcroft-Karp finds max matching:

    "augmenting path" = a path from a free left node to a free right node,
    alternating: unmatched edge -> matched edge -> unmatched edge -> ...
    If we flip all edges on this path (matched <-> unmatched), we get +1 matched pair.

    1. BFS from all free left nodes: find if shortest augmenting paths exist, layer by layer
    2. DFS along those layers: flip edges on augmenting paths to grow matching
    3. Repeat until BFS finds no more augmenting paths
"""

def solve(node_hateNodes_map) -> int:
    """ Time: O(e * sqrt(v)), e = total edges, v = len(node_hateNodes_map)
        Space: O(v + e)
    """
    if len(node_hateNodes_map) == 0: return -1

    left_nodes, right_nodes = _bipartite_partition(node_hateNodes_map)
    matching_count = _hopcroft_karp(node_hateNodes_map, left_nodes, right_nodes)

    return len(node_hateNodes_map) - matching_count


def _bipartite_partition(node_hateNodes_map):
    """ BFS 2-coloring to split nodes into left and right sets
        Time: O(v + e), v = len(node_hateNodes_map), e = total edges
        Space: O(v)
    """
    from collections import deque

    node_color_map = {}
    left_nodes = set()
    right_nodes = set()

    for start_node in node_hateNodes_map:
        if start_node in node_color_map: continue

        node_color_map[start_node] = 0
        left_nodes.add(start_node)
        queue = deque([start_node])

        while queue:
            node = queue.popleft()

            for hate_node in node_hateNodes_map[node]:
                if hate_node in node_color_map: continue

                node_color_map[hate_node] = 1 - node_color_map[node]

                if node_color_map[hate_node] == 0:
                    left_nodes.add(hate_node)
                else:
                    right_nodes.add(hate_node)

                queue.append(hate_node)

    return left_nodes, right_nodes


def _hopcroft_karp(node_hateNodes_map, left_nodes, right_nodes):
    """ Hopcroft-Karp maximum bipartite matching
        Time: O(e * sqrt(v)), e = total edges, v = total nodes
        Space: O(v)
    """
    from collections import deque

    left_match_map = {node: None for node in left_nodes}
    right_match_map = {node: None for node in right_nodes}

    matching_count = 0

    while True:

        # BFS: seed with all free (unmatched) left nodes at layer 0
        node_distance_map = {}
        queue = deque()

        for node in left_nodes:
            if left_match_map[node] is None:
                node_distance_map[node] = 0
                queue.append(node)

        has_augmenting = False

        # explore alternating: left -> unmatched edge -> right -> matched edge -> left ...
        while queue:
            left_node = queue.popleft()

            for right_node in node_hateNodes_map[left_node]:
                matched_node = right_match_map[right_node]

                # right_node is free = end of augmenting path found
                if matched_node is None:
                    has_augmenting = True

                # right_node is matched: follow matched edge back to its left partner, next layer
                elif matched_node not in node_distance_map:
                    node_distance_map[matched_node] = node_distance_map[left_node] + 1
                    queue.append(matched_node)

        if not has_augmenting: break

        # DFS: walk along BFS layers to find and flip augmenting paths
        def _dfs(left_node):
            for right_node in node_hateNodes_map[left_node]:
                matched_node = right_match_map[right_node]

                # flip if: right_node is free, or its matched partner is in next layer and recurse succeeds
                if matched_node is None or (
                    matched_node in node_distance_map
                    and node_distance_map[matched_node] == node_distance_map[left_node] + 1
                    and _dfs(matched_node)
                ):
                    left_match_map[left_node] = right_node
                    right_match_map[right_node] = left_node
                    return True

            # dead end: remove so future DFS calls skip this node
            del node_distance_map[left_node]
            return False

        for node in left_nodes:
            if left_match_map[node] is None:
                if _dfs(node):
                    matching_count += 1

    return matching_count


# Test by "i hate you" edges input
def test(edges):

    def _build_hate_graph(edges):
        ans = {}
        for a, b in edges:
            ans.setdefault(a, []); ans.setdefault(b, [])
            ans[a].append(b); ans[b].append(a)
        return ans

    ans = solve(_build_hate_graph(edges))
    return ans


if __name__ == "__main__":
    assert test([]) == -1

    # 2 nodes, 1 edge (same as tree)
    assert test([(0, 1)]) == 1

    # path of 4 (same as tree: linked list)
    assert test([(0, 1), (1, 2), (2, 3)]) == 2

    # star shaped (same as tree)
    assert test([(0, 1), (0, 2), (0, 3), (0, 4), (0, 5)]) == 5

    # complete bipartite K(2,3): max matching = 2, MIS = 5 - 2 = 3
    edges = [(0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4)]
    assert test(edges) == 3

    # cycle of 6 (bipartite, NOT a tree): max matching = 3, MIS = 6 - 3 = 3
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0)]
    assert test(edges) == 3

    # multiple components: K(1,2) + K(1,1): max matching = 2, MIS = 5 - 2 = 3
    edges = [(0, 1), (0, 2), (3, 4)]
    assert test(edges) == 3
