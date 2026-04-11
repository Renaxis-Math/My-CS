"""
Design a class that maintains the most recent k numbers and supports:
Constraints:
1. When the window exceeds k, the oldest number is evicted.
2. get_mean must be O(1).
3. get_max must be O(1) amortized → use a monotonic deque.
"""

from collections import deque
class Streaming:

	def __init__(self, k):
		self.total = 0.0
	
		# self.count = 0
		# self.cur_max = -float('inf')

		self.val_freq_map = {}
		self.max_freq = 0
		self.maxFreq_val = -float('inf')
		
		# NEW
		self.k = k
		self.mono_desc_window = deque()
		self.window = deque()

	def insert(self, x: float) -> None:
		self.total += x

        # [.... old-max] -> if meet new-max, all old-max died (popright)
		while True:
			if len(self.mono_desc_window) == 0: break
			if not (x > self.mono_desc_window[-1]): break
			self.mono_desc_window.pop()
		
		self.mono_desc_window.append(x)
		self.window.append(x)
		
		return

	def _remove_expired(self):

		while True:
			if len(self.window) <= self.k: return
		
			expired_val = self.window.popleft()
			self.total -= expired_val

            # [expired-time ...] -> popleft
			if (
				self.mono_desc_window and
				self.mono_desc_window[0] == expired_val
			):	
				self.mono_desc_window.popleft()

		return
	
	# NEW
	def get_mean(self):
		if not self.window: return None

		self._remove_expired()
		return self.total / len(self.window)
	
	# NEW
	def get_max(self):
		self._remove_expired()

		if not self.mono_desc_window: return None
		return self.mono_desc_window[0]