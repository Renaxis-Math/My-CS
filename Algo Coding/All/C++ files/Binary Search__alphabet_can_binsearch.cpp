"""
Search Suggestions System
LeetCode 1397 - Difficulty: Medium

You are given an array of strings 'products' and a string 'searchWord'.

Design a system that suggests at most three product names from 'products' after each character of 'searchWord' is typed. Suggested products should have common prefix with 'searchWord'. If there are more than three products with a common prefix return the three lexicographically minimums products.

Return a list of lists of the suggested products after each character of 'searchWord' is typed.



Constraints:

• '1 <= products.length <= 1000'

• '1 <= products[i].length <= 3000'

• '1 <= sum(products[i].length) <= 2 * 10^4'

• All the strings of 'products' are unique.

• 'products[i]' consists of lowercase English letters.

• '1 <= searchWord.length <= 1000'

• 'searchWord' consists of lowercase English letters.
"""



template<class Pred>
int binary_search(int start_i, int end_i, const Pred& in_right_region) {
    int left_i = start_i, right_i = end_i;
    while (left_i <= right_i) {
        int mid_i = left_i + (right_i - left_i) / 2;
        if (in_right_region(mid_i)) right_i = mid_i - 1;
        else left_i = mid_i + 1;
    }
    return left_i;
}

vector<vector<string>> solve(vector<string>& products, string searchWord) {
    sort(products.begin(), products.end());

    vector<vector<string>> answers;
    
    string prefix;
    for (char ch : searchWord) {
        prefix.push_back(ch);
        vector<string> ans;

        // Find the 1st string >= prefix
        int start_i = binary_search(0, products.size() - 1, [&](int mid_i) {
            return products[mid_i] >= prefix;
        });
        
        int count = 0;
        for (int i = start_i; i < products.size() && count < 3; ++i) {
            // only add to ans if the found matches.
            if (products[i].compare(0, prefix.size(), prefix) == 0) {
                ans.push_back(products[i]);
                ++count;
            }
        }

        answers.push_back(ans);
    }

    return answers;
}

class Solution {
public:
    vector<vector<string>> suggestedProducts(vector<string>& products, string searchWord) {
        return solve(products, searchWord);   
    }
};