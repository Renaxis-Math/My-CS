"""
Implement a queue with:

push(uuid, x)
pop(uuid)
get_mean(uuid)

where each operation is tagged with an increasing UUID, 
and get_mean(uuid) should return the mean of the queue at that snapshot.
"""

using namespace std;
using ll = long long;

template<typename T>
using Pair = pair<T, T>;

class VersionMeanQueue {
    queue<int> q;
    ll sum = 0;

    queue<
}