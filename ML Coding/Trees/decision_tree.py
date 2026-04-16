import math
from collections import Counter

class DecisionTree:

	def __init__(self, max_depth=3, min_samples_split=2):
		self.max_depth = max_depth
		self.min_samples_split = min_samples_split
		self.root = {}
		self.x_sorted = []
		self.y_sorted = []

	def fit(self, x: list[float], y: list[int]):
		sorted_tuples = sorted(zip(x, y), key=lambda t: t[0])
		if len(sorted_tuples) == 0:
			self.x_sorted, self.y_sorted, self.root = [], [], {"is_leaf": True, "value": None}
			return self

		self.x_sorted, self.y_sorted = zip(*sorted_tuples)
		self.root = self._build(0, len(self.x_sorted), 0)
		return self

	def _leaf_value(self, lo, hi):
		return Counter(self.y_sorted[i] for i in range(lo, hi)).most_common(1)[0][0]

	def _build(self, lo, hi, depth):
		n = hi - lo
		if n == 0:
			return {"is_leaf": True, "value": None}

		if depth >= self.max_depth or n < self.min_samples_split:
			return {"is_leaf": True, "value": self._leaf_value(lo, hi)}

		max_gain, threshold, split_idx = self._get_maxGain_threshold(lo, hi)

		if max_gain <= 0.0 or threshold is None or split_idx is None:
			return {"is_leaf": True, "value": self._leaf_value(lo, hi)}

		return {
			"is_leaf": False,
			"threshold": threshold,
			"left": self._build(lo, split_idx, depth + 1),
			"right": self._build(split_idx, hi, depth + 1)
		}

	def _clogc(self, freq):
		return 0.0 if freq <= 0 else freq * math.log2(freq)

	def _update(self, mapping, label, delta):
		old_freq = mapping["freq_map"].get(label, 0)
		new_freq = old_freq + delta

		mapping["S"] += self._clogc(new_freq) - self._clogc(old_freq)
		mapping["count"] += delta

		if new_freq == 0:
			mapping["freq_map"].pop(label, None)
		else:
			mapping["freq_map"][label] = new_freq
		return

	def _get_maxGain_threshold(self, lo, hi):
		n = hi - lo
		if n <= 1:
			return (0.0, None, None)

		prefix_map = {"freq_map": Counter(), "count": 0, "S": 0.0}

		suffix_freq_map = Counter(self.y_sorted[i] for i in range(lo, hi))
		suffix_map = {
			"freq_map": suffix_freq_map,
			"count": n,
			"S": sum(self._clogc(freq) for freq in suffix_freq_map.values())
		}

		parent_entropy = max(0.0, math.log2(n) - suffix_map["S"] / n)

		best_gain, best_threshold, best_split_idx = 0.0, None, None

		for end in range(lo, hi - 1):
			label = self.y_sorted[end]
			self._update(prefix_map, label, 1)
			self._update(suffix_map, label, -1)

			xL = self.x_sorted[end]
			xR = self.x_sorted[end + 1]
			if xL == xR:
				continue

			left_n, right_n = prefix_map["count"], suffix_map["count"]
			left_entropy = max(0.0, math.log2(left_n) - prefix_map["S"] / left_n)
			right_entropy = max(0.0, math.log2(right_n) - suffix_map["S"] / right_n)

			gain = parent_entropy - (left_n / n) * left_entropy - (right_n / n) * right_entropy
			if gain > best_gain:
				best_gain = gain
				best_threshold = (xL + xR) / 2.0
				best_split_idx = end + 1

		return (best_gain, best_threshold, best_split_idx)

	def predict(self, x_test_vals: list[float]) -> list[int]:
		def _predict_one(x_test):
			node = self.root
			while node["is_leaf"] == False:
				node = node["left"] if x_test <= node["threshold"] else node["right"]
			return node["value"]

		return [_predict_one(x_test) for x_test in x_test_vals]
