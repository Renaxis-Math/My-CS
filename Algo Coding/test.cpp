"""
Design Circular Queue
LeetCode 860 - Difficulty: Medium

Design your implementation of the circular queue. The circular queue is a linear data structure in which the operations are performed based on FIFO (First In First Out) principle, and the last position is connected back to the first position to make a circle. It is also called "Ring Buffer".

One of the benefits of the circular queue is that we can make use of the spaces in front of the queue. In a normal queue, once the queue becomes full, we cannot insert the next element even if there is a space in front of the queue. But using the circular queue, we can use the space to store new values.

Implement the 'MyCircularQueue' class:

• 'MyCircularQueue(k)' Initializes the object with the size of the queue to be 'k'.

• 'int Front()' Gets the front item from the queue. If the queue is empty, return '-1'.

• 'int Rear()' Gets the last item from the queue. If the queue is empty, return '-1'.

• 'boolean enQueue(int value)' Inserts an element into the circular queue. Return 'true' if the operation is successful.

• 'boolean deQueue()' Deletes an element from the circular queue. Return 'true' if the operation is successful.

• 'boolean isEmpty()' Checks whether the circular queue is empty or not.

• 'boolean isFull()' Checks whether the circular queue is full or not.

You must solve the problem without using the built-in queue data structure in your programming language. 



Constraints:

• '1 <= k <= 1000'

• '0 <= value <= 1000'

• At most '3000' calls will be made to 'enQueue', 'deQueue', 'Front', 'Rear', 'isEmpty', and 'isFull'.
"""

#include<vector>
using namespace std;

class MyCircularQueue {

    vector<int> q;
    int capacity;
    int head_i; // head_i = where old value be de-queued
    int tail_i; // tail_i = where new value will be inserted

    public:
        MyCircularQueue(int k) : 
            capacity{k + 1}, q(k + 1),
            head_i{0}, tail_i{0} // head = tail means empty
        {}
        
        bool enQueue(int value) {
            if (isFull()) return false;

            q[tail_i] = value;
            tail_i = _get_next_write_index(tail_i);
            return true;
        }

        int _get_next_write_index(int tail_i) { 
            return (tail_i + 1) % capacity;
        }
        
        bool deQueue() {
            if (isEmpty()) return false;

            head_i = _get_next_write_index(head_i);
            return true;
        }
        
        int Front() {
            if (isEmpty()) return -1;
            return q[head_i];
        }
        
        int Rear() {
            if (isEmpty()) return -1;

            // avoid negative index e.g. tail = -1 -> tail = size - 1
            return q[(tail_i - 1 + capacity) % capacity];
        }
        
        bool isEmpty() {
            return head_i == tail_i;    
        }
        
        bool isFull() {
            // if head_i is next write index, we can't have overlap -> is full.
            return _get_next_write_index(tail_i) == head_i;
        }
};

/**
 * Your MyCircularQueue object will be instantiated and called as such:
 * MyCircularQueue* obj = new MyCircularQueue(k);
 * bool param_1 = obj->enQueue(value);
 * bool param_2 = obj->deQueue();
 * int param_3 = obj->Front();
 * int param_4 = obj->Rear();
 * bool param_5 = obj->isEmpty();
 * bool param_6 = obj->isFull();
 */