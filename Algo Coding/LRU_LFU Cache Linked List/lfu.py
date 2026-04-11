from collections import defaultdict

class Node:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None
        self.freq = 1

class LFUCache:
    # Time: O(1) per get / put; Space: O(capacity)

    def __init__(self, capacity):
        self.capacity = capacity
        self.key_node_map = {}

        self.freq_HeadTail_map = {}   # freq -> (dummy head, dummy tail)
        self.freq_size = defaultdict(int)

        self.min_freq = float('inf')
    
    def get(self, key):
        if key not in self.key_node_map:
            return -1
        
        node = self.key_node_map[key]
        self._move_to_new_freq(node)
        return node.value
    
    def put(self, key, value):
        if self.capacity == 0:
            return
        
        if key in self.key_node_map:
            node = self.key_node_map[key]
            node.value = value
            self._move_to_new_freq(node)
        
        else:
            if len(self.key_node_map) == self.capacity:
                lfu_head, lfu_tail = self._get_dummies(self.min_freq)
                remove_node = lfu_tail.prev   # LRU among LFU nodes

                self._remove(remove_node, lfu_head, lfu_tail)
                del self.key_node_map[remove_node.key]

                self.freq_size[self.min_freq] -= 1
                if self.freq_size[self.min_freq] == 0:
                    del self.freq_HeadTail_map[self.min_freq]

            node = Node(key, value)
            self.key_node_map[key] = node

            new_head, _ = self._get_dummies(1)
            self._insert_after(new_head, node)

            self.freq_size[1] += 1
            self.min_freq = 1

    """ IDEA
    1. remove node from old freq list
    2. decrement old freq size
    3. update min_freq if needed
    4. increment node freq
    5. insert into new freq list
    6. increment new freq size
    """
    def _move_to_new_freq(self, node):
        old_freq = node.freq
        new_freq = old_freq + 1

        old_head, old_tail = self._get_dummies(old_freq)
        self._remove(node, old_head, old_tail)
        self.freq_size[old_freq] -= 1

        if self.freq_size[old_freq] == 0:
            del self.freq_HeadTail_map[old_freq]
            if self.min_freq == old_freq:
                self.min_freq = new_freq

        node.freq = new_freq
        new_head, _ = self._get_dummies(new_freq)
        self._insert_after(new_head, node)
        self.freq_size[new_freq] += 1

    def _get_dummies(self, freq):
        if freq not in self.freq_HeadTail_map:
            head = Node(); tail = Node()
            
            head.next = tail; tail.prev = head
            self.freq_HeadTail_map[freq] = (head, tail)

        return self.freq_HeadTail_map[freq]

    def _insert_after(self, node, new_node):
        if not (node and new_node):
            return

        right_node = node.next
        new_node.next = right_node
        new_node.prev = node

        node.next = new_node
        right_node.prev = new_node

    def _remove(self, node, dummy_head, dummy_tail):
        if not (node and node != dummy_head and node != dummy_tail):
            return

        left_node = node.prev
        right_node = node.next

        left_node.next = right_node
        right_node.prev = left_node
        
        node.next = None
        node.prev = None