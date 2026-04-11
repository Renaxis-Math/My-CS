class Node:
    def __init__(self, key = None, value = None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    # Time: O(1) per get / put; # Space: O(capacity)

    def __init__(self, capacity):
        self.capacity = capacity
        self.key_node_map = {}
        
        self.dummy_head = Node()  # most recently used side
        self.dummy_tail = Node()  # least recently used side
        self.dummy_head.next = self.dummy_tail
        self.dummy_tail.prev = self.dummy_head
    
    def get(self, key):
        if key not in self.key_node_map: return -1

        node = self.key_node_map[key]

        self._remove(node, self.dummy_head, self.dummy_tail)
        self._insert_after(self.dummy_head, node)
    
        return node.value
    
    def put(self, key, value):
        if self.capacity == 0: return

        if key in self.key_node_map:
            node = self.key_node_map[key]
            
            node.value = value
            self._remove(node, self.dummy_head, self.dummy_tail)

        else:
            if len(self.key_node_map) == self.capacity:
                lru_node = self.dummy_tail.prev

                del self.key_node_map[lru_node.key]
                self._remove(lru_node, self.dummy_head, self.dummy_tail)

            node = Node(key, value)
            self.key_node_map[key] = node
        
        self._insert_after(self.dummy_head, node)
        
        return

    def _insert_after(self, node, new_node):
        if not (node and new_node): return

        left_node = node
        right_node = node.next

        new_node.next = right_node
        new_node.prev = left_node

        left_node.next = new_node
        right_node.prev = new_node

        return

    def _remove(self, node, dummy_head, dummy_tail):
        if not (node and node != dummy_head and node != dummy_tail): return

        left_node = node.prev
        right_node = node.next

        left_node.next = right_node
        right_node.prev = left_node
        
        node.next = None; node.prev = None
        
        return