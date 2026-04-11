"""
Length of Longest Subarray With at Most K Frequency
LeetCode 3225 - Difficulty: Medium

You are given an integer array 'nums' and an integer 'k'.

The frequency of an element 'x' is the number of times it occurs in an array.

An array is called good if the frequency of each element in this array is less than or equal to 'k'.

Return the length of the longest good subarray of 'nums'.

A subarray is a contiguous non-empty sequence of elements within an array.



Constraints:

• '1 <= nums.length <= 10^5'

• '1 <= nums[i] <= 10^9'

• '1 <= k <= nums.length'
"""

#include<vector>
#include<deque>
#include<algorithm>
#include<unordered_map>

using namespace std;

int solve(vector<int> nums, int k) {
    if (!k) return 0;

    int ans = 1;

    unordered_map<int, deque<int>> num_indices_map;

    int left_i = 0; bool is_subarray_false = false;
    for (int right_i = 0; right_i < nums.size(); ++right_i) {
        auto& indices = num_indices_map[nums[right_i]];
        indices.push_back(right_i);

        is_subarray_false = (
            indices.size() > k &&
            // # indices from most recent >= left_i to now > k
            indices[(indices.size() - 1) - k] >= left_i
        );
        if (is_subarray_false) {
            // make it true
            int new_left_i = indices[(indices.size() - 1) - k] + 1;
            left_i = new_left_i;
        }

        ans = max(ans, right_i - left_i + 1);
    }

    return ans;
}