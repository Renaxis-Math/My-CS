#include<vector>
#include<cstddef>
using namespace std;

int solve(vector<int>& nums1, vector<int>& nums2) {
    vector<int> answers1; answers1.reserve(2);
    vector<int> answers2; answers2.reserve(2);
    int final_ans = 1;

    for (size_t i = 0; i < nums1.size(); ++i) {
        size_t dp_i = i;

        int ans1, ans2;
        
        if (i == 0) ans1 = 1, ans2 = 1;

        else {
            ans1 = 1, ans2 = 1;
            if (nums1[i] >= nums1[i-1])
                ans1 = max(ans1, 1 + answers1[(dp_i - 1) % 2]);
            if (nums1[i] >= nums2[i-1])
                ans1 = max(ans1, 1 + answers2[(dp_i - 1) % 2]);             
            
            if (nums2[i] >= nums2[i-1])
                ans2 = max(ans2, 1 + answers2[(dp_i - 1) % 2]);
            if (nums2[i] >= nums1[i-1])
                ans2 = max(ans2, 1 + answers1[(dp_i - 1) % 2]);
        }

        answers1[dp_i % 2] = ans1, answers2[dp_i % 2] = ans2;
        final_ans = max(final_ans, max(ans1, ans2));
    }

    return final_ans;
}

class Solution {
public:
    int maxNonDecreasingLength(vector<int>& nums1, vector<int>& nums2) {
        return solve(nums1, nums2);
    }
};