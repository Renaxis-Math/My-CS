class UF:
    def __init__(self):
        self.node_parent_map = {}
        self.root_size_map = {}

    def union(self, a, b):
        root1, root2 = self.find(a), self.find(b)
        if root1 == root2: return

        size1 = self.root_size_map[root1]
        size2 = self.root_size_map[root2]
        
        smaller_root = root1 if size1 < size2 else root2
        bigger_root = root2 if smaller_root == root1 else root1

        self.node_parent_map[smaller_root] = bigger_root
        self.root_size_map[bigger_root] += self.root_size_map[smaller_root]
        del self.root_size_map[smaller_root]

        return
    
    def find(self, node):
        if node not in self.node_parent_map:
            self.node_parent_map[node] = node
            self.root_size_map[node] = 1

        if self.node_parent_map[node] == node: return node        
        # path compression
        self.node_parent_map[node] = self.find(self.node_parent_map[node])
        return self.node_parent_map[node]