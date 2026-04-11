"""
Reconstruct Itinerary
LeetCode 332 - Difficulty: Hard

You are given a list of airline 'tickets' where 'tickets[i] = [from_i, to_i]' represent the departure and the arrival airports of one flight. Reconstruct the itinerary in order and return it.

All of the tickets belong to a man who departs from '"JFK"', thus, the itinerary must begin with '"JFK"'. If there are multiple valid itineraries, you should return the itinerary that has the smallest lexical order when read as a single string.

• For example, the itinerary '["JFK", "LGA"]' has a smaller lexical order than '["JFK", "LGB"]'.

You may assume all tickets form at least one valid itinerary. You must use all the tickets once and only once.



Constraints:

• '1 <= tickets.length <= 300'

• 'tickets[i].length == 2'

• 'from_i.length == 3'

• 'to_i.length == 3'

• 'from_i' and 'to_i' consist of uppercase English letters.

• 'from_i != to_i'
"""

#include<vector>
#include<string>
#include<unordered_map>
using namespace std;

vector<string> solve(vector<vector<string>>& tickets) {
    unordered_map<string, vector<string>> graph;
    graph.reserve(2 * tickets.size());

    sort(tickets.rbegin(), tickets.rend()); // desc. sort
    for (auto& ticket : tickets)
        graph[ticket[0]].emplace_back(ticket[1]);

    auto euler_dfs = [&]( // O(E)
        auto&& euler_dfs, const string& node, 
        vector<string>& routes) -> void {
        
        /* Euler Path DFS is just dfs but with
        neighbor options changing (reduced) in size. */
        
        // modify-able
        vector<string>& neighbors = graph[node];
        while(!neighbors.empty()) {
            string next_node = neighbors.back();
            neighbors.pop_back();

            euler_dfs(euler_dfs, next_node, routes);
        }
        routes.push_back(node);
    };

    vector<string> routes;
    euler_dfs(euler_dfs, "JFK", routes);
    reverse(routes.begin(), routes.end());
    return routes;
}