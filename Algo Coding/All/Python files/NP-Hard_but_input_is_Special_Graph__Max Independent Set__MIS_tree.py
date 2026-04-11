"""
Given a graph of "i hate you" between people
ensuring the relationships are hierarchical 
and the resulting graph is an undirected, connected tree, 
what is the maximum number of people I can select s.t no one hates each other ?

Input (assumes all nodes exists as keys): 

{
    <node> : [<hate_node>, ...],
    ...
}
"""

""" IDEA: dfs + 2 dp 1d arrays

why 2 dp 1d arrays: 
    you need to represent, for each node u, two different optimal values:
        1. dp(if pick u, parent not picked): u is allowed to be picked
        2. best(if not pick u, parent picked): u is forbidden (because parent was picked)

Note: dfs + dp on tree uses 2 dp 1d a lot since 
on a tree, the only interaction between a u and the rest of the tree is just (parent, u). 
The decision made at the parent (picked or not) constrains whether u can be picked. 
That constraint changes the optimal value inside u's subtree.
"""

def solve(node_hateNodes_map) -> int:
    if len(node_hateNodes_map) == 0: return -1

    # answers for [u...], including u
    pickIt_answers = [1 for _ in range(max(node_hateNodes_map.keys()) + 1)]

    # answers for [u...], NOT including u
    loseIt_answers = [0 for _ in range(max(node_hateNodes_map.keys()) + 1)]

    def dfs(node, parent_node):

        pickIt_ans = pickIt_answers[node]
        loseIt_ans = loseIt_answers[node]

        for hate_node in node_hateNodes_map[node]:

            # trick to avoid repetition (going back up) in undirected tree
            if hate_node == parent_node: continue

            dfs(hate_node, node)

            # collect all cases since tree -> cross-edge doesn't exists

            # if pick node, child must NOT be picked
            pickIt_ans += loseIt_answers[hate_node]

            # if not pick node, child can be pick or not picked
            loseIt_ans += max(pickIt_answers[hate_node], loseIt_answers[hate_node])

        pickIt_answers[node] = pickIt_ans
        loseIt_answers[node] = loseIt_ans

        return

    # since we're given 1) undirected, 2) connected tree
    # -> pick any node as starting point root
    # -> use next(iter(...)) to avoid creating a new list
    random_node = next(iter(node_hateNodes_map.keys()))
    dfs(random_node, None)

    return max(pickIt_answers[random_node], loseIt_answers[random_node])

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

    # 2 nodes, 1 edge
    assert test([(0, 1)]) == 1

    # a linked list of 4 nodes
    assert test([(0, 1), (1, 2), (2, 3)]) == 2

    # star shaped (center = 0)
    assert test([(0, 1), (0, 2), (0, 3), (0, 4), (0, 5)]) == 5

    # path then star. expected 6 (e.g., {-1, 1, 2, 3, 4, 5})
    assert test([(-2, -1), (-1, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5)]) == 6

    # general tree
    edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (4, 6), (4, 7)]
    assert test(edges) == 5
    # expected: 5   (e.g., {0,3,5,6,7})
