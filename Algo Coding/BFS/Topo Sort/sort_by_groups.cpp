"""
Sort Items by Groups Respecting Dependencies
LeetCode 1309 - Difficulty: Hard

There are 'n' items each belonging to zero or one of 'm' groups where 'groups[i]' is the groups that the 'i'-th item belongs to and it's equal to '-1' if the 'i'-th item belongs to no groups. The items and the groups are zero indexed. A groups can have no item belonging to it.

Return a sorted list of the items such that:

• The items that belong to the same groups are next to each other in the sorted list.

• There are some relations between these items where 'before_items[i]' is a list containing all the items that should come before the 'i'-th item in the sorted array (to the left of the 'i'-th item).

Return any solution if there is more than one solution and return an empty list if there is no solution.



Constraints:

• '1 <= m <= n <= 3 * 10^4'

• 'groups.length == before_items.length == n'

• '-1 <= groups[i] <= m - 1'

• '0 <= before_items[i].length <= n - 1'

• '0 <= before_items[i][j] <= n - 1'

• 'i != before_items[i][j]'

• 'before_items[i] 'does not contain duplicates elements.
"""

#include <vector>
#include <deque>
#include <unordered_set>
using namespace std;

vector<int> _topo_sort(int nodes_count, vector<vector<int>>& graph, vector<int> in_degrees);

vector<int> solve(
    int items_count,
    int groups_count,
    vector<int>& groups,
    vector<vector<int>>& before_items
) {
    // 1) assign new groups to every ungroupsed item, extending 'groups'
    for (int item = 0; item < items_count; ++item) {
        if (groups[item] == -1) groups[item] = groups_count++;
    }

    // 2) build item graph + groups graph
    vector<vector<int>> item_graph(items_count);
    vector<int> item_in_degrees(items_count, 0);

    vector<vector<int>> groups_graph(groups_count);
    vector<int> groups_in_degrees(groups_count, 0);

    vector<unordered_set<int>> groups_edge_sets(groups_count);

    for (int item = 0; item < items_count; ++item) {
        for (int i = 0; i < before_items[item].size(); ++i) {
            int prev_item = before_items[item][i];

            // item edge
            item_graph[prev_item].emplace_back(item);
            item_in_degrees[item]++;

            // groups edge
            int prev_groups = groups[prev_item], cur_groups = groups[item];
            if (prev_groups != cur_groups && !groups_edge_sets[prev_groups].contains(cur_groups)) {
                groups_edge_sets[prev_groups].insert(cur_groups);
                groups_graph[prev_groups].emplace_back(cur_groups);
                groups_in_degrees[cur_groups]++;
            }
        }
    }

    // 3) topo sort groups + items
    vector<int> groups_order = _topo_sort(groups_count, groups_graph, groups_in_degrees);
    vector<int> item_order = _topo_sort(items_count, item_graph, item_in_degrees);

    // 4) bucket items by groups using item topo order
    vector<vector<int>> ordered_groups_items(groups_count);
    for (int i = 0; i < item_order.size(); ++i) {
        int item = item_order[i];
        ordered_groups_items[groups[item]].emplace_back(item);
    }

    // 5) output groups in topo order
    vector<int> answers; answers.reserve(items_count);
    for (int i = 0; i < groups_order.size(); ++i) {
        int cur_groups = groups_order[i];

        for (int j = 0; j < ordered_groups_items[cur_groups].size(); ++j) {
            answers.emplace_back(ordered_groups_items[cur_groups][j]);
        }
    }

    return (answers.size() == items_count) ? answers : vector<int>{};
}


vector<int> _topo_sort(int nodes_count, vector<vector<int>>& graph, vector<int> in_degrees) {
    deque<int> queue;
    for (int node_i = 0; node_i < nodes_count; ++node_i) {
        if (!in_degrees[node_i]) queue.emplace_back(node_i);
    }

    vector<int> answers; answers.reserve(nodes_count);

    while (!queue.empty()) {
        int node_i= queue.front(); queue.pop_front();
        answers.emplace_back(node_i);

        for (int i = 0; i < graph[node_i].size(); ++i) {
            int next_node_i = graph[node_i][i];

            in_degrees[next_node_i]--;
            if (!in_degrees[next_node_i]) queue.emplace_back(next_node_i);
        }
    }

    return (answers.size() == nodes_count) ? answers : vector<int>{};
}