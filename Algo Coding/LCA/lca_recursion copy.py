class Node:
    def __init__(self, val, left = None, right = None):
        self.val = val
        self.left = left
        self.right = right

"""
Time Complexity: O(n)
Space Complexity: O(height of tree)
"""
def solve(root: Node, a: Node, b: Node):
    target_needed = 2 if a != b else 1

    def dfs(node):  # -> (lca_node, foundTarget_count)
        if node is None: return (None, 0)

        foundTarget_count = (node in [a, b])
        for child in [node.left, node.right]:
            child_lca, child_found = dfs(child)

            # If any sub-lca found return immediately
            if child_lca: return (child_lca, child_found)
            foundTarget_count += child_found

        # if only 1 target exists -> still Fail
        ans = node if foundTarget_count >= target_needed else None
        return (ans, foundTarget_count)

    ans, foundTarget_count = dfs(root)
    return ans


""" n-ary tree, k targets version
class Node:
    # Avoid Python gotcha: every Node shares the same list object. 
    # Appending a child to one node mutates all nodes’ children.
    def __init__(self, val, children = None):
        self.val = val
        self.children = children or []

def solve_general(root: Node, targets: list[Node]):
    targets_set = set(targets)
    target_needed = len(targets_set)

    def dfs(node):  # -> (lca_node, foundTarget_count)
        if node is None: return (None, 0)

        foundTarget_count = (node in targets_set)
        for child in node.children:
            child_lca, child_found = dfs(child)

            # If any sub-lca found return immediately
            if child_lca: return (child_lca, child_found)
            foundTarget_count += child_found

        # if only 1 target exists -> still Fail
        ans = node if foundTarget_count >= target_needed else None
        return (ans, foundTarget_count)

    ans, foundTarget_count = dfs(root)
    return ans
"""