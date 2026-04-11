"""
Palindromic Substrings
LeetCode 647 - Difficulty: Medium

Given a string 's', return the number of palindromic substrings in it.

A string is a palindrome when it reads the same backward as forward.

A substring is a contiguous sequence of characters within the string.



Constraints:

• '1 <= s.length <= 1000'

• 's' consists of lowercase English letters.
"""

#include<iostream>
#include<vector>
using namespace std;

#define FOR(i, a, b, step) for (int i = a; i < b; i += step)
#define ROF(i, a, b, step) for (int i = a; i >= b; i -= step)

int solve(string& s) {
    vector<vector<int>> answers(s.size(), vector<int>(s.size(), 0));
    int final_ans = 0;

    ROF(start_i, s.size() - 1, 0, 1) {
        FOR(end_i, start_i, s.size(), 1) {

            int dp_start_i = start_i, dp_end_i = end_i;

            int ans = answers[dp_start_i][dp_end_i];

            if (dp_start_i > dp_end_i) ans = 0;
            else if (dp_start_i == dp_end_i) ans = 1;
            else if (dp_end_i == dp_start_i + 1) {
                ans = (s[start_i] == s[end_i]) ? 1 : 0;
            }
            else {
                ans = (s[start_i] == s[end_i]) ?
                        answers[start_i + 1][end_i - 1] : 0;
            }

            answers[dp_start_i][dp_end_i] = ans;
            final_ans += ans;
        }
    }

    return final_ans;
}