"""
Parallel Courses III
LeetCode 2176 - Difficulty: Hard

You are given an integer 'n', which indicates that there are 'n' courses labeled from '1' to 'n'. You are also given a 2D integer array 'relations' where 'relations[j] = [prevCourse_j, nextCourse_j]' denotes that course 'prevCourse_j' has to be completed before course 'nextCourse_j' (prerequisite relationship). Furthermore, you are given a 0-indexed integer array 'time' where 'time[i]' denotes how many months it takes to complete the '(i+1)^th' course.

You must find the minimum number of months needed to complete all the courses following these rules:

• You may start taking a course at any time if the prerequisites are met.

• Any number of courses can be taken at the same time.

Return the minimum number of months needed to complete all the courses.

Note: The test cases are generated such that it is possible to complete every course (i.e., the graph is a directed acyclic graph).



Constraints:

• '1 <= n <= 5 * 10^4'

• '0 <= relations.length <= min(n * (n - 1) / 2, 5 * 10^4)'

• 'relations[j].length == 2'

• '1 <= prevCourse_j, nextCourse_j <= n'

• 'prevCourse_j != nextCourse_j'

• All the pairs '[prevCourse_j, nextCourse_j]' are unique.

• 'time.length == n'

• '1 <= time[i] <= 10^4'

• The given graph is a directed acyclic graph.
"""

void _topo_sort(
    int nodes_count, vector<vector<int>>& graph, vector<int> in_degrees,
    vector<int>& times, vector<int>& reach_times
);

int solve(int nodes_count, vector<vector<int>>& relations, vector<int>& times) {

    // build directed src -> [dest, ...] graph and in-degrees
    vector<vector<int>> graph(nodes_count);
    vector<int> in_degrees(nodes_count, 0);

    for (auto& edge : relations) {
        int src_i = edge[0] - 1, dest_i = edge[1] - 1;
        graph[src_i].emplace_back(dest_i);
        in_degrees[dest_i]++;
    }

    // bfs to find min time = time to reach right-most lowest depth node = max(reach_times)
    vector<int> reach_times(nodes_count, 0);

    _topo_sort(nodes_count, graph, in_degrees, times, reach_times);
    return *max_element(reach_times.begin(), reach_times.end());
}

void _topo_sort(
    int nodes_count, vector<vector<int>>& graph, vector<int> in_degrees,
    vector<int>& times, vector<int>& reach_times) {
    
    // vector<int> answers; answers.reserve(nodes_count);
    
    deque<int> queue;
    for (int node_i = 0; node_i < nodes_count; ++node_i) {
        if (!in_degrees[node_i]) {
            queue.emplace_back(node_i);
            reach_times[node_i] = times[node_i];
        }
    }

    while (!queue.empty()) {     
        int node_i = queue.front(); queue.pop_front();

        for (int i = 0; i < graph[node_i].size(); ++i) {
            int next_node_i = graph[node_i][i];

            reach_times[next_node_i] = max(
                reach_times[next_node_i], reach_times[node_i] + times[next_node_i]
            );

            in_degrees[next_node_i]--;
            if (!in_degrees[next_node_i]) queue.emplace_back(next_node_i);
        }
    }

    // return (answers.size() == nodes_count) ? answers : vector<int>{};
}