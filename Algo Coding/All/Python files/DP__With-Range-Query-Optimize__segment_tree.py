class SegTree:
    # sum segment tree, point-add update, inclusive query [ql, qr]
    # leaf for rank r is at tree node index: n + r
    def __init__(self, max_rank):
        self.last_leave_i = max_rank + 1
        self.tree = [0] * (2 * self.last_leave_i)
        self.rank_nodeIndex_map = {r: r + self.last_leave_i for r in range(self.last_leave_i)}
        self.root_i = 1

    def update(self, rank, delta):

        # Step 1: Update leaf mapped by rank
        node_i = self.rank_nodeIndex_map[rank]
        self.tree[node_i] += delta

        # Step 2: Update parent building up
        while node_i >= self.root_i:
            node_i //= 2    # go to parent: [4,5] -> 2
            self.tree[node_i] = self.tree[node_i*2] + self.tree[node_i*2 + 1]

    def query(self, query_low_rank, query_high_rank):

        # Invalid case
        if query_low_rank > query_high_rank:
            return 0 # we want sum -> 0
        
        # Norma case
        low_node_i = self.rank_nodeIndex_map[query_low_rank]
        high_node_i = self.rank_nodeIndex_map[query_high_rank]

        ans = 0

        def _is_right_child(node_i):
            return node_i % 2 == 1
        def _is_left_child(node_i):
            return node_i % 2 == 0

        while low_node_i <= high_node_i:
            
            # Left edge case: 
            # - low_node_i is right child
            # - left child is out of range
            if _is_right_child(low_node_i):
                ans += self.tree[low_node_i]

                # shrink the range to avoid duplicate sum in parent
                low_node_i += 1
            
            # Right edge case
            if _is_left_child(high_node_i):
                ans += self.tree[high_node_i]

                # shrink the range
                high_node_i -= 1
            
            low_node_i //= 2; high_node_i //= 2

        return ans


