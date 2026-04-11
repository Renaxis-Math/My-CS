/*
You have an array of integers nums (0-indexed) and two integer values x and y. 
You can perform operations on this array to reduce all numbers to zero or below.

In each operation, you:

Choose any index i from the array (where 0 <= i < nums.length)
Decrease the value at nums[i] by x
Decrease the values at all other indices (every position except i) by y
Your goal is to find the minimum number of operations needed to make every integer in nums less than or equal to zero.

For example, if you have nums = [10, 5, 8], x = 4, and y = 1, 
and you perform one operation choosing index 0:

nums[0] decreases by 4: 10 - 4 = 6
nums[1] decreases by 1: 5 - 1 = 4
nums[2] decreases by 1: 8 - 1 = 7
Result after operation: [6, 4, 7]
You would continue performing operations until all values become <= 0. 
The problem asks for the minimum number of such operations required.
*/

#include <algorithm>
#include <vector>
using namespace std;

using ll = long long;

template<class Pred>
int binary_search(int start, int end, Pred in_right_region) {
    int left = start, right = end;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (in_right_region(mid)) right = mid - 1;
        else left = mid + 1;
    }
    return left;
}

// DO NOT use built-in ceil or abs
int ceil(ll numerator, ll denominator) {
    return (numerator + denominator - 1) / denominator;
}

int abs(ll a, ll b) { return (a < b) ? b - a : a - b; }

int solve(vector<int>& nums, int x, int y) {
    int ans = 0;

    if (nums.size() == 1) return ceil(nums[0], x);

    if (x == y) {
        for (int num : nums)
            ans = max(ans, ceil(num, x));
    }
    
    else {
        auto is_feasible = [&](int max_ops_count) {
            if (x > y) {
                ll ops_count = 0;

                for (int& num : nums) {
                    ll rem_positive_count = num - (ll) y * max_ops_count;
                    ops_count += (rem_positive_count > 0) ? ceil(rem_positive_count, x - y) : 0;
                }

                return ops_count <= max_ops_count;
            } 
            
            // If x < y, each time an index is chosen, 
            // it'ss penalized by y - x relative to not being chosen, 
            // so you compute a max allowed # ops
            else {

                // if total allowed chooses are enough to cover all operations.
                ll total_allowed_chooses = 0;

                for (int& num : nums) {
                    ll rem = (ll) y * max_ops_count - num;
                    if (rem < 0) return false;
                    total_allowed_chooses += rem / (y - x);
                }

                return total_allowed_chooses >= max_ops_count;
            }
        };

        int max_num = *max_element(nums.begin(), nums.end());
        ans = binary_search(0, max_num, is_feasible);
    }

    return ans;
}
