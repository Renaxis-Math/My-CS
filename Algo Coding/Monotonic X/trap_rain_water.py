"""
Trapping Rain Water
LeetCode 42 - Difficulty: Hard

Given 'n' non-negative integers representing an elevation map where the width of each bar is '1', compute how much water it can trap after raining.



Constraints:

• 'n == height.length'

• '1 <= n <= 2 * 10^4'

• '0 <= height[i] <= 10^5'
"""

from collections import deque

def solve(heights) -> int:
    ans = 0

    earliest_to_right_peaks = _get_earliest_peaks(heights, True)
    earliest_to_left_peaks = _get_earliest_peaks(heights, False)

    for i, height in enumerate(heights):
        to_left_peak = earliest_to_left_peaks[i]
        to_right_peak = earliest_to_right_peaks[i]

        ans += max(0, (min(to_left_peak, to_right_peak) - height))
    
    return ans

def _get_earliest_peaks(heights, is_left_to_right: bool):
    answers = [-1] * len(heights)

    start_i = 0 if is_left_to_right else len(heights) - 1
    past_end_i = len(heights) if is_left_to_right else -1

    mono_stack = deque() # mono non-increase queue: [(val1, val1 >= val2, ...]
    for i in range(start_i, past_end_i, 1 if is_left_to_right else -1):
        while (mono_stack and mono_stack[-1] < heights[i]):
            mono_stack.pop()
        mono_stack.append(heights[i])

        answers[i] = mono_stack[0]

    return answers
