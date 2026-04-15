#include "unique_ptr.h"
#include<iostream>
#include<cassert>
#include<string>

struct Box {
    int value;

    Box(int v) : value{v} {}
    void set(int v) { value = v; }
};

int main() {
    /* 1) Test default constructor */
    {
        UniquePtr<int> p;
        assert(p.get() == nullptr);
        assert(!p);
    }

    /* 2) Test constructor from raw pointer */
    {
        UniquePtr<int> p(new int(42));
        assert(p.get() != nullptr);
        assert(*p == 42);
        assert(p);
    }

    /* 3) Test operator* */
    {
        UniquePtr<int> p(new int(10));
        *p = 99;
        assert(*p == 99);
    }

    /* 4) Test operator-> */
    {
        UniquePtr<Box> p(new Box(5));
        assert(p->value == 5);

        p->set(20);
        assert(p->value == 20);
    }

    /* 5) Test get() */
    {
        UniquePtr<int> p(new int(7));
        int* raw = p.get();

        assert(raw != nullptr);
        assert(*raw == 7);

        // p still owns raw here        
    }

    /* 6) Test bool conversion */
    {
        UniquePtr<int> p1;
        UniquePtr<int> p2(new int(1));

        assert(!p1);
        assert(p2);
    }
    
    /* 7) Test move constructor */
    {
        UniquePtr<int> p(new int(55));
        UniquePtr<int> q(std::move(p));
        assert(!p);
        assert(q);
        assert(*q == 55);
    }

    /* 8) Test move assignment */
    {
        UniquePtr<int> p(new int(11));
        UniquePtr<int> q(new int(22));

        q = std::move(p);

        assert(!p);
        assert(q);
        assert(*q == 11);
    }

    /* 9) Test release() */
    {
        UniquePtr<int> p(new int(88));
        int* raw = p.release();

        assert(!p);
        assert(p.get() == nullptr);
        assert(raw != nullptr);
        assert(*raw == 88);

        delete raw; // must manually delete after release()
    }

    /* 10) Test reset(new pointer) */
    {
        UniquePtr<int> p(new int(3));
        p.reset(new int(9));

        assert(p);
        assert(*p == 9);
    }

    /* 11) Test reset() to nullptr */
    {
        UniquePtr<int> p(new int(100));
        p.reset();

        assert(!p);
        assert(p.get() == nullptr);
    }

    /* 12) Test swap() */
    {
        UniquePtr<int> a(new int(1));
        UniquePtr<int> b(new int(2));

        a.swap(b);

        assert(*a == 2);
        assert(*b == 1);
    }

    /* 13) Test self move assignment */
    {
        UniquePtr<int> p(new int(77));
        p = std::move(p);

        assert(p);
        assert(*p == 77);
    }

    std::cout << "Passed All Test!\n";
    return 0;
}