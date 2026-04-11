"""
Combination Sum
LeetCode 39 - Difficulty: Medium

Given an array of distinct integers 'candidates' and a target integer 'target', return a list of all unique combinations of 'candidates' where the chosen numbers sum to 'target'. You may return the combinations in any order.

The same number may be chosen from 'candidates' an unlimited number of times. Two combinations are unique if the frequency of at least one of the chosen numbers is different.

The test cases are generated such that the number of unique combinations that sum up to 'target' is less than '150' combinations for the given input.



Constraints:

• '1 <= candidates.length <= 30'

• '2 <= candidates[i] <= 40'

• All elements of 'candidates' are distinct.

• '1 <= target <= 40'
"""

vector<vector<int>> solve(vector<int>& candidates, int target) {
    vector<vector<int>> answers;

    // get only unique values in 'candidates'
    unordered_set<int> seen_candidates;
    vector<int> unique_candidates;
    unique_candidates.reserve(candidates.size());
    for (int cand : candidates) {
        if (seen_candidates.insert(cand).second) unique_candidates.emplace_back(cand);
    }

    // ascending sort (a must) for faster pruning
    sort(unique_candidates.begin(), unique_candidates.end());

    
    /* IDEA: DFS */
    auto backtrack = [&](auto&& self,
        size_t i, int cur_target, vector<int>& sub_answers) {
        // base case
        if (cur_target == 0) {
            answers.push_back(sub_answers);
            return;
        }

        for (size_t next_i = i; next_i < unique_candidates.size(); ++next_i) {

            // break instead of continue for pruning
            if (cur_target - unique_candidates[next_i] < 0) break;
            
            sub_answers.emplace_back(unique_candidates[next_i]);
            self(self, next_i, cur_target - unique_candidates[next_i], sub_answers);
            sub_answers.pop_back();
        }
    };

    vector<int> sub_answers;
    backtrack(backtrack, 0, target, sub_answers);
    return answers;
}