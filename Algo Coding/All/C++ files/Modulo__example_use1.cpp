"""
Smallest Missing Non-negative Integer After Operations
LeetCode 2661 - Difficulty: Medium

You are given a 0-indexed integer array 'nums' and an integer 'value'.

In one operation, you can add or subtract 'value' from any element of 'nums'.

• For example, if 'nums = [1,2,3]' and 'value = 2', you can choose to subtract 'value' from 'nums[0]' to make 'nums = [-1,2,3]'.

The MEX (minimum excluded) of an array is the smallest missing non-negative integer in it.

• For example, the MEX of '[-1,2,3]' is '0' while the MEX of '[1,0,3]' is '2'.

Return the maximum MEX of 'nums' after applying the mentioned operation any number of times.



Constraints:

• '1 <= nums.length, value <= 10^5'

• '-10^9 <= nums[i] <= 10^9'
"""

/* IDEA (read top -> bottom)
1) Operation keeps modulo class:
   if we do nums[i] + m * value, then nums[i] % value never changes.

2) Therefore each nums[i] belongs to exactly one modulo group:
   group_i = ((nums[i] % value) + value) % value
   modulo_group_sizes[group_i]++

3) Very important:
   group index is only in [0 .. value - 1].
   There is NO separate "group 5" when value = 5.
   Example value = 5:
   - 0, 5, 10, 15 ... are all in group 0
   - 1, 6, 11, 16 ... are all in group 1
   - 2, 7, 12, 17 ... are all in group 2
   ...

4) Build answer from ans = 0 upward:
   To form number ans, we need one unused element from group (ans % value).

5) If modulo_group_sizes[ans % value] > 0:
   we can form ans -> consume one copy:
   modulo_group_sizes[ans % value]--, then ans++.

6) First ans where needed group has 0 copies left:
   cannot form ans -> that ans is the smallest missing non-negative integer.
*/

int solve(vector<int>& nums, int value) {

    // Get all the group sizes by modulo: observation:
    // as we take modulo, answer options can't exceed 'value'
    vector<int> modulo_group_sizes(value, 0);
    for (int i = 0; i < (int)nums.size(); ++i) {
        int group_i = ((nums[i] % value) + value) % value;
        modulo_group_sizes[group_i]++;
    }

    // Find answer
    int ans = 0;
    while (modulo_group_sizes[ans % value] > 0) {
        modulo_group_sizes[ans % value]--;
        ans++;
    }
    
    return ans;
}