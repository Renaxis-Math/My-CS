#include "space_memory_pool.h"
#include <cassert>
#include <iostream>
#include <string>

struct Box {
    int value = 0;
    void set(int v) { value = v; }
};

int main() {
    /* 1) Test initial state */
    {
        MemoryPool<int, 3> pool;
        assert(pool.capacity() == 3);
        assert(pool.available() == 3);
        assert(pool.empty());
        assert(!pool.full());
    }

    /* 2) Test first allocation */
    {
        MemoryPool<int, 3> pool;
        int* p = pool.allocate();

        assert(p != nullptr);
        assert(pool.capacity() == 3);
        assert(pool.available() == 2);
        assert(!pool.empty());
        assert(!pool.full());
    }

    /* 3) Test writing through allocated pointer */
    {
        MemoryPool<int, 2> pool;
        int* p = pool.allocate();

        assert(p != nullptr);
        *p = 42;
        assert(*p == 42);
        assert(pool.available() == 1);
    }

    /* 4) Test multiple allocations */
    {
        MemoryPool<int, 3> pool;

        int* a = pool.allocate();
        int* b = pool.allocate();
        int* c = pool.allocate();

        assert(a != nullptr);
        assert(b != nullptr);
        assert(c != nullptr);

        assert(a != b);
        assert(b != c);
        assert(a != c);

        assert(pool.available() == 0);
        assert(pool.full());
        assert(!pool.empty());
    }

    /* 5) Test allocation when full */
    {
        MemoryPool<int, 2> pool;

        int* a = pool.allocate();
        int* b = pool.allocate();
        int* c = pool.allocate();

        assert(a != nullptr);
        assert(b != nullptr);
        assert(c == nullptr);

        assert(pool.available() == 0);
        assert(pool.full());
    }

    /* 6) Test deallocation returns one slot */
    {
        MemoryPool<int, 2> pool;

        int* a = pool.allocate();
        int* b = pool.allocate();

        assert(a != nullptr);
        assert(b != nullptr);
        assert(pool.available() == 0);

        bool ok = pool.deallocate(a);
        assert(ok);
        assert(pool.available() == 1);
        assert(!pool.full());
        assert(!pool.empty());
    }

    /* 7) Test deallocated slot can be reused */
    {
        MemoryPool<int, 2> pool;

        int* a = pool.allocate();
        int* b = pool.allocate();

        assert(a != nullptr);
        assert(b != nullptr);

        assert(pool.deallocate(a));
        int* c = pool.allocate();

        assert(c != nullptr);
        assert(c == a);           // freed slot reused
        assert(pool.available() == 0);
    }

    /* 8) Test LIFO reuse behavior */
    {
        MemoryPool<int, 3> pool;

        int* a = pool.allocate();
        int* b = pool.allocate();
        int* c = pool.allocate();

        assert(a && b && c);

        assert(pool.deallocate(b));
        assert(pool.deallocate(c));

        int* x = pool.allocate();
        int* y = pool.allocate();

        assert(x == c);           // most recently freed comes back first
        assert(y == b);
    }

    /* 9) Test deallocate nullptr */
    {
        MemoryPool<int, 3> pool;

        bool ok = pool.deallocate(nullptr);
        assert(!ok);

        assert(pool.available() == 3);
        assert(pool.empty());
    }

    /* 10) Test deallocate pointer not from pool */
    {
        MemoryPool<int, 3> pool;
        int outside = 10;

        bool ok = pool.deallocate(&outside);
        assert(!ok);

        assert(pool.available() == 3);
        assert(pool.empty());
    }

    /* 11) Test double free protection */
    {
        MemoryPool<int, 3> pool;
        int* p = pool.allocate();

        assert(p != nullptr);

        bool first = pool.deallocate(p);
        bool second = pool.deallocate(p);

        assert(first);
        assert(!second);
        assert(pool.available() == 3);
        assert(pool.empty());
    }

    /* 12) Test pool with struct type */
    {
        MemoryPool<Box, 2> pool;

        Box* a = pool.allocate();
        Box* b = pool.allocate();

        assert(a != nullptr);
        assert(b != nullptr);

        a->set(10);
        b->set(20);

        assert(a->value == 10);
        assert(b->value == 20);
        assert(pool.full());
    }

    /* 13) Test mixed allocate/deallocate sequence */
    {
        MemoryPool<int, 4> pool;

        int* a = pool.allocate();
        int* b = pool.allocate();
        int* c = pool.allocate();

        assert(a && b && c);
        assert(pool.available() == 1);

        assert(pool.deallocate(b));
        assert(pool.available() == 2);

        int* d = pool.allocate();
        int* e = pool.allocate();

        assert(d == b);
        assert(e != nullptr);
        assert(pool.available() == 0);
        assert(pool.full());

        assert(pool.deallocate(a));
        assert(pool.deallocate(c));
        assert(pool.deallocate(d));
        assert(pool.deallocate(e));

        assert(pool.available() == 4);
        assert(pool.empty());
    }

    /* 14) Test all slots reusable after full cycle */
    {
        MemoryPool<int, 3> pool;

        int* a = pool.allocate();
        int* b = pool.allocate();
        int* c = pool.allocate();

        assert(a && b && c);
        assert(pool.full());

        assert(pool.deallocate(a));
        assert(pool.deallocate(b));
        assert(pool.deallocate(c));

        assert(pool.empty());
        assert(pool.available() == 3);

        int* x = pool.allocate();
        int* y = pool.allocate();
        int* z = pool.allocate();

        assert(x != nullptr);
        assert(y != nullptr);
        assert(z != nullptr);
        assert(pool.full());
    }

    /* 15) Test values survive until deallocation */
    {
        MemoryPool<int, 2> pool;

        int* a = pool.allocate();
        int* b = pool.allocate();

        assert(a && b);

        *a = 111;
        *b = 222;

        assert(*a == 111);
        assert(*b == 222);

        assert(pool.deallocate(a));
        assert(pool.deallocate(b));
        assert(pool.empty());
    }

    std::cout << "Passed All Test!\n";
    return 0;
}