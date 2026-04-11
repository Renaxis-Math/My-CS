"""
Evaluate Division
LeetCode 399 - Difficulty: Medium

You are given an array of variable pairs 'equations' and an array of real numbers 'values', where 'equations[i] = [A_i, B_i]' and 'values[i]' represent the equation 'A_i / B_i = values[i]'. Each 'A_i' or 'B_i' is a string that represents a single variable.

You are also given some 'queries', where 'queries[j] = [C_j, D_j]' represents the 'j^th' query where you must find the answer for 'C_j / D_j = ?'.

Return the answers to all queries. If a single answer cannot be determined, return '-1.0'.

Note: The input is always valid. You may assume that evaluating the queries will not result in division by zero and that there is no contradiction.

Note: The variables that do not occur in the list of equations are undefined, so the answer cannot be determined for them.



Constraints:

• '1 <= equations.length <= 20'

• 'equations[i].length == 2'

• '1 <= A_i.length, B_i.length <= 5'

• 'values.length == equations.length'

• '0.0 < values[i] <= 20.0'

• '1 <= queries.length <= 20'

• 'queries[i].length == 2'

• '1 <= C_j.length, D_j.length <= 5'

• 'A_i, B_i, C_j, D_j' consist of lower case English letters and digits.
"""

#include<vector>
#include<unordered_map>
#include<utility>
#include<limits>
using namespace std;

using str_vec = vector<string>;
using edge = pair<string, double>;

double dfs(
    string src_node, string dest_node,
    unordered_map<string, vector<edge>>& graph,
    unordered_set<string>& memo) {
        string key = src_node;
        memo.insert(key);

        if (src_node == dest_node) return 1.0;
        else {
            for (auto& [next_node, weight] : graph.at(src_node)) {
                string next_key = next_node;
                if (memo.find(next_key) == memo.end()) { // not 'seen'
                    double next_ans = dfs(next_node, dest_node, graph, memo);
                    if (next_ans != -1.0) return weight * next_ans;
                }
            }
        }

        // neither 'src' nor any neighbors can find a path to 'dest'
        return -1.0;
}

vector<double> solve(
    vector<str_vec>& equations, 
    vector<double>& values, 
    vector<str_vec>& queries) {

        // Build weighted undirected graph
        unordered_map<string, vector<edge>> graph;
        for (int i = 0; i < equations.size(); ++i) {
            string src = equations[i][0], dest = equations[i][1];
            graph[src].push_back({dest, values[i]});
            if (values[i]) graph[dest].push_back({src, 1/values[i]});
        }

        // get ans by dfs
        vector<double> answers;

        for (auto& query : queries) {
            string src = query[0], dest = query[1];
            if (!graph.count(src) || !graph.count(dest)) {
                answers.push_back(-1.0);
            }
            else {
                unordered_set<string> memo;
                answers.push_back(dfs(src, dest, graph, memo));
            }
        }

        return answers;
}