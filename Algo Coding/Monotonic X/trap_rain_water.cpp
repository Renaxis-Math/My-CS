"""
Trapping Rain Water
LeetCode 42 - Difficulty: Hard

Given 'n' non-negative integers representing an elevation map where the width of each bar is '1', compute how much water it can trap after raining.



Constraints:

• 'n == height.length'

• '1 <= n <= 2 * 10^4'

• '0 <= height[i] <= 10^5'
"""

vector<int> _get_earliest_peaks(vector<int>& heights, bool is_left_to_right);

int solve(vector<int>& heights) {
    int ans = 0;

    vector<int> earliest_to_right_peaks = _get_earliest_peaks(heights, true);
    vector<int> earliest_to_left_peaks = _get_earliest_peaks(heights, false);

    for (int i = 0; i < heights.size(); ++i) {
        int left_peak = earliest_to_left_peaks[i],
            right_peak = earliest_to_right_peaks[i];
        ans += max(0, min(left_peak, right_peak) - heights[i]);
    }

    return ans;
}

/* IDEA: at each i. one side is already “decided.”

Rule for this problem:

* keep `leftMax` and `rightMax`
* if `leftMax <= rightMax`, process left
* else process right

Why is that valid?

Because water at a position is: min(leftMax, rightMax) - height[i]

So if currently: leftMax <= rightMax, 
then for the left pointer, the minimum is already forced to be `leftMax`.
You do not need to know anything more about the right side. 
Even if the right side gets taller later, the min stays `leftMax`.

So the left position is final now. You can consume it and move on.

So the most useful rule is:
Two pointers works when, after comparing left-summary and right-summary, one side becomes final immediately.
*/
int solve_optimal(vector<int>& heights) {
    int ans = 0;

    int left_prefix_max = 0, right_prefix_max = 0;
    
    int left_i = 0, right_i = heights.size() - 1;
    while (left_i <= right_i) {
        if (left_prefix_max <= right_prefix_max) {
            left_prefix_max = max(left_prefix_max, heights[left_i]);
            ans += (left_prefix_max - heights[left_i]);
            left_i++;
        }
        else {
            right_prefix_max = max(right_prefix_max, heights[right_i]);
            ans += (right_prefix_max - heights[right_i]);
            right_i--;
        }
    }

    return ans;
}

vector<int> _get_earliest_peaks(vector<int>& heights, bool is_left_to_right) {
    vector<int> answers(heights.size());

    vector<int> mono_stack; mono_stack.reserve(heights.size());
    if (is_left_to_right) {
        for (int i = 0; i < heights.size(); ++i) {
            while (!mono_stack.empty() && mono_stack.back() < heights[i]) {
                mono_stack.pop_back();
            }
            mono_stack.emplace_back(heights[i]);
            answers[i] = mono_stack[0];
        }
    }
    else {
        for (int i = heights.size() - 1; i > -1; --i) {
            while (!mono_stack.empty() && mono_stack.back() < heights[i]) {
                mono_stack.pop_back();
            }
            mono_stack.emplace_back(heights[i]);
            answers[i] = mono_stack[0];
        }
    }

    return answers;
}