class MinHeap:
    def __init__(self, elements=None):
        # Initializing with a list uses the O(n) "build_heap" method
        self.heap = elements if elements else []
        if self.heap:
            self._build_heap()

    def _build_heap(self):
        n = len(self.heap)
        # Using your formula to find the parent of the last element
        last_child_parent_i = ((n - 1) - 1) // 2
        
        # Start from the last parent and move backwards to the root
        for current_i in range(last_child_parent_i, -1, -1):
            self._sift_down(current_i)

    def _sift_down(self, parent_i):
        n = len(self.heap)
        while True:
            minval_i = parent_i
            left_child_i = 2 * parent_i + 1
            right_child_i = 2 * parent_i + 2
            
            # Check if left child is smaller than current smallest
            if left_child_i < n and self.heap[left_child_i] < self.heap[minval_i]:
                minval_i = left_child_i
            
            # Check if right child is even smaller
            if right_child_i < n and self.heap[right_child_i] < self.heap[minval_i]:
                minval_i = right_child_i
                
            # If the smallest isn't the parent, swap and continue sifting down
            if minval_i != parent_i:
                self.heap[parent_i], self.heap[minval_i] = self.heap[minval_i], self.heap[parent_i]
                parent_i = minval_i
            else: break

    def insert(self, value):
        self.heap.append(value)
        self._sift_up(len(self.heap) - 1)

    def _sift_up(self, child_i):
        parent_i = (child_i - 1) // 2
        while child_i > 0 and self.heap[child_i] < self.heap[parent_i]:
            self.heap[child_i], self.heap[parent_i] = self.heap[parent_i], self.heap[child_i]

            child_i = parent_i
            parent_i = (child_i - 1) // 2

    def pop_min(self):
        if not self.heap: return None
        if len(self.heap) == 1: return self.heap.pop()
        
        root_value = self.heap[0]

        self.heap[0] = self.heap.pop() # Move last element to root
        self._sift_down(0)

        return root_value