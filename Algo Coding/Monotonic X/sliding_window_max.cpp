"""
Sliding Window Maximum
LeetCode 239 - Difficulty: Hard

You are given an array of integers 'nums', there is a sliding window of size 'k' which is moving from the very left of the array to the very right. You can only see the 'k' numbers in the window. Each time the sliding window moves right by one position.

Return the max sliding window.



Constraints:

• '1 <= nums.length <= 10^5'

• '-10^4 <= nums[i] <= 10^4'

• '1 <= k <= nums.length'
"""

#include<vector>
#include<deque>
using namespace std;

vector<int> solve(vector<int>& nums, int k) {
    vector<int> answers;
    answers.reserve(nums.size() - k + 1);

    deque<int> mono_max_dq; // indices: max -> 2nd max -> ...

    for (int i = 0; i < nums.size(); ++i) {

        // remove 'out of bound' left
        int ideal_first_dq_i = i - k + 1;

        while (true) {
            if (mono_max_dq.empty()) break;
            if (mono_max_dq.front() >= ideal_first_dq_i)
                break;
            mono_max_dq.pop_front();
        }

        // remove 'not good enough' from the right
        while (true) {
            if (mono_max_dq.empty()) break;
            if (nums[mono_max_dq.back()] >= nums[i]) break;

            mono_max_dq.pop_back();
        }

        mono_max_dq.push_back(i);

        // only getting answer if we have window size >= k
        if (ideal_first_dq_i >= 0)
            answers.emplace_back(nums[mono_max_dq.front()]);
    }

    return answers;
}