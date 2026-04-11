/*
Merge Intervals
LeetCode 56 - Difficulty: Medium

Given an array of 'intervals' where 'intervals[i] = [start_i, end_i]', merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.



Constraints:

• '1 <= intervals.length <= 10^4'

• 'intervals[i].length == 2'

• '0 <= start_i <= end_i <= 10^4'
*/

#include<vector>
using namespace std;

#include<algorithm>

bool can_merge(vector<int> interval1, vector<int> interval2) {
    return !(
        interval1[1] < interval2[0] ||
        interval2[1] < interval1[0]
    );
}

vector<vector<int>> solve(vector<vector<int>> intervals) {
    if (!intervals.size()) return intervals;

    sort(intervals.begin(), intervals.end(),
        [](vector<int>& a, vector<int>& b) {
           return a[0] < b[0];
        }
    );

    vector<vector<int>> answers;    // stack

    for (int i = 0; i < intervals.size(); ++i) {
        if (!answers.empty() && can_merge(answers.back(), intervals[i])) {
            answers.back() = {
                min(answers.back()[0], intervals[i][0]),
                max(answers.back()[1], intervals[i][1])
            };
        }
        else answers.push_back(intervals[i]);
    }

    return answers;
}