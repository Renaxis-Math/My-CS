import heapq

class Node:
    def __init__(self, freq, char=None, left=None, right=None):
        self.freq = freq
        self.char = char
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

_root = None
_char_code_map = {}

def encode(a_str: str):
    """
    Time Complexity: O(n + m log m)
    Space Complexity: O(m)
    n = len(a_str)
    m = number of unique characters in a_str
    """
    global _root
    global _char_code_map

    if a_str == "":
        _root = None
        _char_code_map = {}
        return ""

    # Build char_freq_map
    char_freq_map = {}
    for char in a_str:
        char_freq_map[char] = char_freq_map.get(char, 0) + 1

    # Add leaves to heap
    node_heap = []
    for char, freq in char_freq_map.items():
        heapq.heappush(node_heap, Node(freq, char=char))

    # Special case: only 1 unique character
    if len(node_heap) == 1:
        _root = node_heap[0]
        _char_code_map = {_root.char: "0"}
        return "0" * len(a_str)

    # Normal case
    while len(node_heap) > 1:
        node1 = heapq.heappop(node_heap)
        node2 = heapq.heappop(node_heap)
        heapq.heappush(node_heap, Node(node1.freq + node2.freq, left=node1, right=node2))

    # Update global variables
    _root = heapq.heappop(node_heap)

    char_code_map = {}
    _build_codes(_root, "", char_code_map)
    _char_code_map = char_code_map

    return "".join(_char_code_map[char] for char in a_str)

def _build_codes(node, prefix_str, char_code_map):
    """
    Time Complexity: O(m)
    Space Complexity: O(h)
    m = number of nodes in the tree (2 * unique_chars - 1)
    h = height of the Huffman tree
    """
    # Base case: leaf
    if node.left is None and node.right is None:
        char_code_map[node.char] = prefix_str
        return

    if node.left is not None:
        _build_codes(node.left, prefix_str + "0", char_code_map)
    if node.right is not None:
        _build_codes(node.right, prefix_str + "1", char_code_map)


def decode(a_bits_str: str):
    """
    Time Complexity: O(L)
    Space Complexity: O(n)
    L = len(a_bits_str)
    n = length of decoded output
    """
    if a_bits_str == "":
        return ""

    if _root is None:
        raise ValueError("decode called before encode")

    # Special case: single-character tree
    if _root.left is None and _root.right is None:
        return _root.char * len(a_bits_str)

    # Normal case
    ans_chars = []
    cur_node = _root

    for bit in a_bits_str:
        assert bit in "01"

        if bit == "0": # go left
            cur_node = cur_node.left
        
        else: # bit == "1" -> go right
            cur_node = cur_node.right

        # reach leave
        if cur_node.left is None and cur_node.right is None:
            ans_chars.append(cur_node.char)
            cur_node = _root

    return "".join(ans_chars)
