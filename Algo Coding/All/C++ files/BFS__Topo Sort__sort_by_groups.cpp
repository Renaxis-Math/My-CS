"""
Sort Items by Groups Respecting Dependencies
LeetCode 1309 - Difficulty: Hard

There are 'n' items each belonging to zero or one of 'm' groups where 'group[i]' is the group that the 'i'-th item belongs to and it's equal to '-1' if the 'i'-th item belongs to no group. The items and the groups are zero indexed. A group can have no item belonging to it.

Return a sorted list of the items such that:

• The items that belong to the same group are next to each other in the sorted list.

• There are some relations between these items where 'beforeItems[i]' is a list containing all the items that should come before the 'i'-th item in the sorted array (to the left of the 'i'-th item).

Return any solution if there is more than one solution and return an empty list if there is no solution.



Constraints:

• '1 <= m <= n <= 3 * 10^4'

• 'group.length == beforeItems.length == n'

• '-1 <= group[i] <= m - 1'

• '0 <= beforeItems[i].length <= n - 1'

• '0 <= beforeItems[i][j] <= n - 1'

• 'i != beforeItems[i][j]'

• 'beforeItems[i] 'does not contain duplicates elements.
"""

#include <vector>
#include <deque>
#include <unordered_set>
using namespace std;

vector<int> _topo_sort(int nodes_count, vector<vector<int>>& graph, vector<int> in_degrees);

vector<int> solve(
    int items_count,
    int groups_count,
    vector<int>& group,
    vector<vector<int>>& beforeItems
) {
    // 1) assign unique group to every ungrouped item
    int next_group = groups_count;
    for (int item = 0; item < items_count; ++item) {
        if (group[item] == -1) group[item] = next_group++;
    }
    groups_count = next_group;

    // 2) build item graph + group graph
    vector<vector<int>> item_graph(items_count);
    vector<int> item_in_degrees(items_count, 0);

    vector<vector<int>> group_graph(groups_count);
    vector<int> group_in_degrees(groups_count, 0);

    vector<unordered_set<int>> group_edge_sets(groups_count);

    for (int item = 0; item < items_count; ++item) {
        for (int i = 0; i < beforeItems[item].size(); ++i) {
            int prev_item = beforeItems[item][i];

            // item edge
            item_graph[prev_item].emplace_back(item);
            item_in_degrees[item]++;

            // group edge
            int prev_group = group[prev_item], cur_group = group[item];
            if (prev_group != cur_group && !group_edge_sets[prev_group].contains(cur_group)) {
                group_edge_sets[prev_group].insert(cur_group);
                group_graph[prev_group].emplace_back(cur_group);
                group_in_degrees[cur_group]++;
            }
        }
    }

    // 3) topo sort groups + items
    vector<int> group_order = _topo_sort(groups_count, group_graph, group_in_degrees);
    if (group_order.empty()) return {};

    vector<int> item_order = _topo_sort(items_count, item_graph, item_in_degrees);
    if (item_order.empty()) return {};

    // 4) bucket items by group using item topo order
    vector<vector<int>> ordered_group_items(groups_count);
    for (int i = 0; i < item_order.size(); ++i) {
        int item = item_order[i];
        ordered_group_items[group[item]].emplace_back(item);
    }

    // 5) output groups in topo order
    vector<int> answers; answers.reserve(items_count);
    for (int i = 0; i < group_order.size(); ++i) {
        int cur_group = group_order[i];

        for (int j = 0; j < ordered_group_items[cur_group].size(); ++j) {
            answers.emplace_back(ordered_group_items[cur_group][j]);
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