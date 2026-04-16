/* IDEA: Since all elements have the same size, you do not need general-purpose heap logic. The clean idea is:
	•	allocate one big block up front
	•	split it into equal-size slots
	•	keep a free list of available slots
	•	allocate() pops one slot from the free list
	•	deallocate() pushes the slot back

That is the standard user-space pool design for same-size elements.

The core intuition:
1. [slot] -> [slot] -> [slot] -> [slot] -> [slot]
      ^ `free` list links unused slots together
2. Each unused slot stores a pointer to the next unused slot.
*/

#include <cstddef>
#include <unordered_map>

template<typename T, std::size_t N>
class MemoryPool {
    struct Node {
        T value{};
        bool in_use = false;
        Node* next = nullptr;
    };

    Node pool[N];
    Node* free_head = nullptr;
    std::size_t available_slots = N;
    std::unordered_map<T*, Node*> where;

public:
    MemoryPool() {
        for (std::size_t i = 0; i < N - 1; ++i) {
            pool[i].next = &pool[i + 1];
        }
        pool[N - 1].next = nullptr;
        free_head = &pool[0];
    }

    constexpr std::size_t capacity() const { return N; }
    std::size_t available() const { return available_slots; }
    bool full() const { return available_slots == 0; }
    bool empty() const { return available_slots == N; }

    T* allocate() {
        if (!free_head) return nullptr;

        Node* chosen = free_head;
        free_head = free_head->next;

        chosen->in_use = true;
        chosen->next = nullptr;
        --available_slots;

        T* ptr = &chosen->value;
        where[ptr] = chosen;
        return ptr;
    }

    bool deallocate(T* ptr) {
        if (!ptr) return false;

        auto it = where.find(ptr);
        if (it == where.end()) return false;

        Node* node = it->second;
        if (!node->in_use) return false;

        node->in_use = false;
        node->next = free_head;
        free_head = node;
        ++available_slots;

        where.erase(it);
        return true;
    }
};