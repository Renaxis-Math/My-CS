class Node:
    def __init__(self, val, left = None, right = None):
        self.val = val
        self.left = left
        self.right = right

"""
Time Complexity: 
    Amortized: O(tree height) ~ O(log n)
    Worst Case: O(n)

Space Complexity: O(1)
"""
def solve(root, a, b):

    while root:
        if a < root.val and b < root.val:
            root = root.left

        elif a > root.val and b > root.val:
            root = root.right

        else:
            return root