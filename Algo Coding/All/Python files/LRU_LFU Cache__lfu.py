# NEVER USE SORTED LIST / DICT built in Python library aka C++'s multiset
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.freq = 1
        self.prev = None
        self.next = None


class LFUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.min_freq = 0
        self.key_node = {}      # key -> node
        self.freq_dummy = {}    # freq -> (head, tail)
        self.freq_size = {}     # freq -> size

    def _make_list(self, freq):
        head = Node(0, 0)
        tail = Node(0, 0)
        head.next = tail
        tail.prev = head
        self.freq_dummy[freq] = (head, tail)
        self.freq_size[freq] = 0

    def _add_to_head(self, freq, node):
        if freq not in self.freq_dummy:
            self._make_list(freq)

        head, tail = self.freq_dummy[freq]
        node.prev = head
        node.next = head.next
        head.next.prev = node
        head.next = node
        self.freq_size[freq] += 1

    def _remove_node(self, node):
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node
        self.freq_size[node.freq] -= 1

    def _pop_tail(self, freq):
        head, tail = self.freq_dummy[freq]
        real_tail = tail.prev
        self._remove_node(real_tail)
        return real_tail

    def _update_freq(self, node):
        old_freq = node.freq
        self._remove_node(node)

        if old_freq == self.min_freq and self.freq_size[old_freq] == 0:
            self.min_freq += 1

        node.freq += 1
        self._add_to_head(node.freq, node)

    def get(self, key):
        if key not in self.key_node:
            return -1

        node = self.key_node[key]
        self._update_freq(node)
        return node.value

    def put(self, key, value):
        if self.capacity == 0:
            return

        if key in self.key_node:
            node = self.key_node[key]
            node.value = value
            self._update_freq(node)
            return

        if len(self.key_node) == self.capacity:
            node_to_remove = self._pop_tail(self.min_freq)
            del self.key_node[node_to_remove.key]

        new_node = Node(key, value)
        self.key_node[key] = new_node
        self.min_freq = 1
        self._add_to_head(1, new_node)

# Your LFUCache object will be instantiated and called as such:
# obj = LFUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)