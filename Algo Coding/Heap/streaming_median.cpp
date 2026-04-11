"""
Find Median from Data Stream
LeetCode 295 - Difficulty: Hard

The median is the middle value in an ordered integer list. If the size of the list is even, there is no middle value, and the median is the mean of the two middle values.

• For example, for 'arr = [2,3,4]', the median is '3'.

• For example, for 'arr = [2,3]', the median is '(2 + 3) / 2 = 2.5'.

Implement the MedianFinder class:

• 'MedianFinder()' initializes the 'MedianFinder' object.

• 'void addNum(int num)' adds the integer 'num' from the data stream to the data structure.

• 'double findMedian()' returns the median of all elements so far. Answers within '10^-5' of the actual answer will be accepted.



Constraints:

• '-10^5 <= num <= 10^5'

• There will be at least one element in the data structure before calling 'findMedian'.

• At most '5 * 10^4' calls will be made to 'addNum' and 'findMedian'.



Follow up:

• If all integer numbers from the stream are in the range '[0, 100]', how would you optimize your solution?

• If '99%' of all integer numbers from the stream are in the range '[0, 100]', how would you optimize your solution?
"""

#include<queue>
using namespace std;

class MedianFinder {
public:
    priority_queue<int> max_heap;
    priority_queue<int, vector<int>, greater<int>> min_heap;

    MedianFinder() {}
    
    void addNum(int num) {
        // invariant1: max_heap.top <= min_heap.top()
        if (max_heap.empty() || num <= max_heap.top()) max_heap.push(num);
        else min_heap.push(num);

        // invariant2: |max_heap.size() - min_heap.size()| <= 1
        if (max_heap.size() > min_heap.size() + 1) {
            min_heap.push(max_heap.top()); max_heap.pop();
        }
        if (min_heap.size() > max_heap.size() + 1) {
            max_heap.push(min_heap.top()); min_heap.pop();
        }
    }
    
    double findMedian() {
        if (max_heap.size() == min_heap.size()) {
            return (max_heap.top() + min_heap.top()) / 2.0;
        }
        else {  // size diff == 1
            return max_heap.size() > min_heap.size() ? max_heap.top() : min_heap.top();
        }
    }
};

/**
 * Your MedianFinder object will be instantiated and called as such:
 * MedianFinder* obj = new MedianFinder();
 * obj->addNum(num);
 * double param_2 = obj->findMedian();
 */