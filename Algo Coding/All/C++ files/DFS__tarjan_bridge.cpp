"""
Critical Connections in a Network
LeetCode 1300 - Difficulty: Hard

There are 'n' servers numbered from '0' to 'n - 1' connected by undirected server-to-server 'connections' forming a network where 'connections[i] = [a_i, b_i]' represents a connection between servers 'a_i' and 'b_i'. Any server can reach other servers directly or indirectly through the network.

A critical connection is a connection that, if removed, will make some servers unable to reach some other server.

Return all critical connections in the network in any order.



Constraints:

• '2 <= n <= 10^5'

• 'n - 1 <= connections.length <= 10^5'

• '0 <= a_i, b_i <= n - 1'

• 'a_i != b_i'

• There are no repeated connections.
"""

#include <vector>
using namespace std;

vector<vector<int>> solve(int nodes_count, vector<vector<int>>& connections) {
    // build undirected graph
    vector<vector<int>> graph(nodes_count);
    for (auto& edge : connections) {
        int a = edge[0], b = edge[1];
        graph[a].push_back(b);
        graph[b].push_back(a);
    }

    // first_reach_times[node] = DFS discovery time of node
    // min_reach_times[node]   = earliest discovery time reachable from node/subtree
    vector<int> first_reach_times(nodes_count, -1);
    vector<int> min_reach_times(nodes_count, -1);

    vector<vector<int>> answers;
    int timer = 0;

    auto dfs = [&](auto&& dfs, int node, int parent) -> void {
        // first time we ever reach this node in DFS
        first_reach_times[node] = timer;
        min_reach_times[node] = timer;
        timer++;

        for (int i = 0; i < graph[node].size(); ++i) {
            int next_node = graph[node][i];

            // don't go immediately back through the same undirected edge
            if (next_node == parent) continue;

            // Case 1: tree edge (not visited yet)
            if (first_reach_times[next_node] == -1) {
                dfs(dfs, next_node, node);

                // after child DFS finishes, child subtree may know an older node
                // reachable through some back-edge
                min_reach_times[node] = min(
                    min_reach_times[node],
                    min_reach_times[next_node]
                );

                // critical edge condition:
                // if child subtree cannot reach this node or any ancestor of this node,
                // then removing (node, next_node) disconnects the graph
                if (min_reach_times[next_node] > first_reach_times[node]) {
                    answers.push_back({node, next_node});
                }
            }

            // Case 2: back edge to an already-visited node
            else {
                // IMPORTANT: for a back-edge, update with first_reach_times[next_node],
                // not min_reach_times[next_node]
                min_reach_times[node] = min(
                    min_reach_times[node],
                    first_reach_times[next_node]
                );
            }
        }
    };

    // graph is connected in LC 1192, but this loop makes the helper more general
    for (int node = 0; node < nodes_count; ++node) {
        if (first_reach_times[node] == -1) {
            dfs(dfs, node, -1);
        }
    }

    return answers;
}

class Solution {
public:
    vector<vector<int>> criticalConnections(int n, vector<vector<int>>& connections) {
        return solve(n, connections);
    }
};