"""
Find Servers That Handled Most Number of Requests
LeetCode 1710 - Difficulty: Hard

You have 'k' servers numbered from '0' to 'k-1' that are being used to handle multiple requests simultaneously. Each server has infinite computational capacity but cannot handle more than one request at a time. The requests are assigned to servers according to a specific algorithm:

• The 'i^th' (0-indexed) request arrives.

• If all servers are busy, the request is dropped (not handled at all).

• If the '(i % k)^th' server is available, assign the request to that server.

• Otherwise, assign the request to the next available server (wrapping around the list of servers and starting from 0 if necessary). For example, if the 'i^th' server is busy, try to assign the request to the '(i+1)^th' server, then the '(i+2)^th' server, and so on.

You are given a strictly increasing array 'arrival' of positive integers, where 'arrival[i]' represents the arrival time of the 'i^th' request, and another array 'load', where 'load[i]' represents the load of the 'i^th' request (the time it takes to complete). Your goal is to find the busiest server(s). A server is considered busiest if it handled the most number of requests successfully among all the servers.

Return a list containing the IDs (0-indexed) of the busiest server(s). You may return the IDs in any order.



Constraints:

• '1 <= k <= 10^5'

• '1 <= arrival.length, load.length <= 10^5'

• 'arrival.length == load.length'

• '1 <= arrival[i], load[i] <= 10^9'

• 'arrival' is strictly increasing.
"""

template<class T>
using MinHeap = priority_queue<T, vector<T>, greater<T>>;

using pii = pair<int, int>;

int modulo(int x, int mod) { return ((x % mod) + mod) % mod; }

vector<int> solve(vector<int>& arrive_times, vector<int>& complete_times, int k) {

    MinHeap<pii> busy;                  // (end time, server i)
    MinHeap<int> free_geq_i, free_lt_i; // (free server i % k)

    vector<int> server_assignCounts(k, 0);

    // Block 1: Push all k servers to free, prioritize >= i heap over < i
    for (int server = 0; server < k; ++server) free_geq_i.push(server);
    
    // Block 2: Simulation for each request
    for (int req_i = 0; req_i < arrive_times.size(); ++req_i) {
        int target_server = modulo(req_i, k);

        // 2.1) pop additional available servers from busy
        while (!busy.empty() && busy.top().first <= arrive_times[req_i]) {
            pii ele = busy.top(); busy.pop();
            int end_time = ele.first, new_free_server = ele.second;

            // allocate accordingly
            if (new_free_server >= target_server) {
                free_geq_i.push(modulo(new_free_server, k));
            }
            else free_lt_i.push(modulo(new_free_server, k));
        }

        // 2.2) as modulo can change index, we do internal free heap transfer
        while (!free_geq_i.empty() && free_geq_i.top() < target_server) {
            free_lt_i.push(free_geq_i.top());
            free_geq_i.pop();
        }
        while (!free_lt_i.empty() && free_lt_i.top() >= target_server) {
            free_geq_i.push(free_lt_i.top());
            free_lt_i.pop();
        }

        // 2.3) get the most recent free server, prioritize >= i over < i
        MinHeap<int>& free_heap = (free_geq_i.empty()) ? free_lt_i : free_geq_i;
        if (!free_heap.empty()) {
            int free_server = free_heap.top();
            int end_time = arrive_times[req_i] + complete_times[req_i];

            server_assignCounts[free_server]++;
            busy.push({end_time, free_server});
            free_heap.pop();
        }
    }

    int max_assign_count = *max_element(server_assignCounts.begin(), server_assignCounts.end());
    
    vector<int> answers; answers.reserve(k);
    for (int server = 0; server < server_assignCounts.size(); ++server) {
        if (server_assignCounts[server] == max_assign_count) answers.emplace_back(server);
    }

    return answers;
}

class Solution {
public:
    vector<int> busiestServers(int k, vector<int>& arrival, vector<int>& load) {
        return solve(arrival, load, k);
    }
};