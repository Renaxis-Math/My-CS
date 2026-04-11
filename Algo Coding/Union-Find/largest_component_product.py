"""
You are given a set of friends identified by 1-based indices.
There are several unordered pairs of friends and each pair belongs to a particular company identified by an integer.

For a specific company, consider the graph that contains only the pairs whose company id matches that company.
The vertices of the graph are the friends that appear in those pairs, edges are the pairs themselves.

Your task is to determine, across all companies, the greatest product of 
2 friend ids of the largest connected component.
If more than one component shares that maximum size, y
ou must compute the greatest product of the two friend ids 
that belong to the same component among those tied components.

Return that product.
If a component has fewer than two friends, its product is defined as zero.

Input:
n = number of friends
friend_tuples = [(a, b, company_id), ...]
"""

def solve(n_friend, friend_tuples):
    # Time: O(E * α(V)) ≈ O(E), Space: O(E)
    # E = len(friend_tuples), V = distinct friends    

    # Time: O(E * α(V))
    companyId_uf_map = {}
    for [a, b, company_id] in friend_tuples:
        if company_id not in companyId_uf_map: companyId_uf_map[company_id] = UF()
        companyId_uf_map[company_id].union(a, b)
    
    # Time: O(# of uf = # of companies)
    biggest_size = 0
    for uf in companyId_uf_map.values():
        biggest_size = max(biggest_size, uf.top_size)


    # Time: O(total # uf nodes across all companies)
    #     = O(2 * total # edges)
    #     = O(2 * len(friend_tuples))
    tied_components = []
    for uf in companyId_uf_map.values():
        for root, size in uf.root_size_map.items():
            if size == biggest_size:
                tied_components.append(uf.root_top2id_map[root])

    best_product = 0
    for top2 in tied_components:
        best_product = max(best_product, top2[0] * top2[1])

    return best_product

class UF:
    def __init__(self):
        self.node_parent_map = {}
        self.root_size_map = {}
        self.root_top2id_map = {}
        self.top_size = 0

    def union(self, a, b):
        # Time: amortized α(...)

        root1, root2 = self.find(a), self.find(b)
        if root1 == root2: return

        size1 = self.root_size_map[root1]
        size2 = self.root_size_map[root2]

        root1_top2ids = self.root_top2id_map[root1]
        root2_top2ids = self.root_top2id_map[root2]
        
        smaller_root = root1 if size1 < size2 else root2
        bigger_root = root2 if smaller_root == root1 else root1

        self.node_parent_map[smaller_root] = bigger_root
        self.root_size_map[bigger_root] += self.root_size_map[smaller_root]
        del self.root_size_map[smaller_root]

        self.root_top2id_map[bigger_root] = self._find_new_top_ids(root1_top2ids, root2_top2ids)
        del self.root_top2id_map[smaller_root]
        self.top_size = max(self.top_size, self.root_size_map[bigger_root])

        return
    
    def find(self, node):
        # Time: amortized α(...)
        
        if node not in self.node_parent_map:
            self.node_parent_map[node] = node
            self.root_size_map[node] = 1
            self.root_top2id_map[node] = [node, 0]
            self.top_size = max(self.top_size, 1)
            return node

        if self.node_parent_map[node] == node: return node
        
        # path compression
        self.node_parent_map[node] = self.find(self.node_parent_map[node])
        return self.node_parent_map[node]

    def _find_new_top_ids(self, root1_top2ids, root2_top2ids):
        ids = root1_top2ids + root2_top2ids

        top_id = -1; second_top_id = -1
        for id in ids:
            if id > top_id:
                second_top_id = top_id
                top_id = id
            elif id > second_top_id:
                second_top_id = id
        
        return [top_id, second_top_id]

def test():
    assert solve(
        5, [(1, 2, 1), (2, 3, 1), (4, 5, 3), (1, 3, 1)]
    ) == 6