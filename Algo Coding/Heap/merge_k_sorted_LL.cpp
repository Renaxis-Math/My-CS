"""
Merge k Sorted Lists
LeetCode 23 - Difficulty: Hard

You are given an array of 'k' linked-lists 'lists', each linked-list is sorted in ascending order.

Merge all the linked-lists into one sorted linked-list and return it.



Constraints:

• 'k == lists.length'

• '0 <= k <= 10^4'

• '0 <= lists[i].length <= 500'

• '-10^4 <= lists[i][j] <= 10^4'

• 'lists[i]' is sorted in ascending order.

• The sum of 'lists[i].length' will not exceed '10^4'.
"""

#include<queue>
using namespace std;

struct Node {
    int val;
    Node* next;
    Node(int val = 0, Node *next = nullptr) : val(val), next(next) {}
}

// MUST-USE a Compare operator for pointer
// because Node* default comparison compares addresses,
// not node values.
struct Compare {
    // we want min-heap

    // use 'const' after function since “calling this function does not modify the Compare object.”
    bool operator()(Node* a, Node* b) const { return a->val > b->val; }
};

template<class T>
using MinHeap = priority_queue<T, vector<T>, Compare>;

Node* solve(vector<Node*>& lists) {
    MinHeap<Node*> heap;
    for (auto& node : lists) if(node) heap.push(node);

    Node* dummy = new Node(0);
    Node* tail = dummy;

    while (!heap.empty()) {
        Node* node = heap.top();
        heap.pop();

        tail->next = node;
        tail = tail->next;

        if (node->next) heap.push(node->next);
    }
    
    return dummy->next;
}