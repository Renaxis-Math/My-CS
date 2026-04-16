#include "shared_ptr.h"
#include <cassert>
#include <iostream>

struct Box {
    int value;

    Box(int v) : value{v} {}
    void set(int v) { value = v; }
};

int main() {
    /* 1) Test default constructor */
    {
        SharedPtr<int> p;
        assert(p.get() == nullptr);
        assert(!p);
        assert(p.get_count() == 0);
    }

    /* 2) Test constructor from raw pointer */
    {
        SharedPtr<int> p(new int(42));
        assert(p.get() != nullptr);
        assert(*p == 42);
        assert(p);
        assert(p.get_count() == 1);
    }

    /* 3) Test operator* */
    {
        SharedPtr<int> p(new int(10));
        *p = 99;
        assert(*p == 99);
        assert(p.get_count() == 1);
    }

    /* 4) Test operator-> */
    {
        SharedPtr<Box> p(new Box(5));
        assert(p->value == 5);

        p->set(20);
        assert(p->value == 20);
        assert(p.get_count() == 1);
    }

    /* 5) Test get() */
    {
        SharedPtr<int> p(new int(7));
        int* raw = p.get();

        assert(raw != nullptr);
        assert(*raw == 7);

        // p still shares ownership of raw here
        assert(p.get_count() == 1);
    }

    /* 6) Test bool conversion */
    {
        SharedPtr<int> p1;
        SharedPtr<int> p2(new int(1));

        assert(!p1);
        assert(p2);
        assert(p1.get_count() == 0);
        assert(p2.get_count() == 1);
    }

    /* 7) Test copy constructor */
    {
        SharedPtr<int> p(new int(55));
        SharedPtr<int> q(p);

        assert(p);
        assert(q);
        assert(*p == 55);
        assert(*q == 55);
        assert(p.get_count() == 2);
        assert(q.get_count() == 2);
    }

    /* 8) Test copy assignment */
    {
        SharedPtr<int> p(new int(11));
        SharedPtr<int> q(new int(22));

        q = p;

        assert(p);
        assert(q);
        assert(*p == 11);
        assert(*q == 11);
        assert(p.get_count() == 2);
        assert(q.get_count() == 2);
    }

    /* 9) Test move constructor */
    {
        SharedPtr<int> p(new int(88));
        SharedPtr<int> q(std::move(p));

        assert(!p);
        assert(q);
        assert(*q == 88);
        assert(p.get_count() == 0);
        assert(q.get_count() == 1);
    }

    /* 10) Test move assignment */
    {
        SharedPtr<int> p(new int(3));
        SharedPtr<int> q(new int(9));

        q = std::move(p);

        assert(!p);
        assert(q);
        assert(*q == 3);
        assert(p.get_count() == 0);
        assert(q.get_count() == 1);
    }

    /* 11) Test reset(new pointer) */
    {
        SharedPtr<int> p(new int(100));
        p.reset(new int(200));

        assert(p);
        assert(*p == 200);
        assert(p.get_count() == 1);
    }

    /* 12) Test reset() to nullptr */
    {
        SharedPtr<int> p(new int(100));
        p.reset();

        assert(!p);
        assert(p.get() == nullptr);
        assert(p.get_count() == 0);
    }

    /* 13) Test swap() */
    {
        SharedPtr<int> a(new int(1));
        SharedPtr<int> b(new int(2));

        a.swap(b);

        assert(*a == 2);
        assert(*b == 1);
        assert(a.get_count() == 1);
        assert(b.get_count() == 1);
    }

    /* 14) Test shared ownership count */
    {
        SharedPtr<int> a(new int(5));
        SharedPtr<int> b = a;
        SharedPtr<int> c = a;

        assert(a.get_count() == 3);
        assert(b.get_count() == 3);
        assert(c.get_count() == 3);
        assert(*a == 5);
        assert(*b == 5);
        assert(*c == 5);
    }

    /* 15) Test self copy assignment */
    {
        SharedPtr<int> p(new int(77));
        p = p;

        assert(p);
        assert(*p == 77);
        assert(p.get_count() == 1);
    }

    /* 16) Test self move assignment */
    {
        SharedPtr<int> p(new int(123));
        p = std::move(p);

        assert(p);
        assert(*p == 123);
        assert(p.get_count() == 1);
    }

    std::cout << "Passed All Test!\n";
    return 0;
}