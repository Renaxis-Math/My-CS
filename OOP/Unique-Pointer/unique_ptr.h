#include<utility>
#include<cassert>

template<typename T>
class UniquePtr {
    T* ptr = nullptr;

    public:
        constexpr UniquePtr() = default;
        // don't want implicit type conversions since wrappers are independent
        explicit UniquePtr(T* p) : ptr{p} {}


        /* Rule of 3 */

        // No copy nor copy assignment wanted, since unique ownership
        UniquePtr(const UniquePtr& other) = delete;
        UniquePtr& operator=(const UniquePtr& other) = delete;
        // Your class owns a resource, so you must explicitly release it
        // -> don't use `= default`: it destroys the UniquePtr object, not the `ptr` field.
        ~UniquePtr() { delete ptr; }


        /* Rule of 5 (3 + 2 add-on) for std::move() */
        
        UniquePtr(UniquePtr&& other) : 
            ptr{other.ptr}   // transfer ownership
        { 
            other.ptr = nullptr;    // unique owner rule
        }                 

        UniquePtr& operator=(UniquePtr&& other) {
            // Even though `other` has type T&&, it's a named variable, 
            // hence, it's an lvalue expression inside the function.
            if (this != &other) {   // avoid self-deletion
                delete ptr;
                ptr = other.ptr; other.ptr = nullptr;
            }
            return *this;
        }        


        /* Pointer's CORE: itself */
        T* get() const { return ptr; }

        T& operator*() const { assert(ptr); return *ptr; }
        T* operator->() const { assert(ptr); return ptr; }
        
        // for (!unique_ptr)
        explicit operator bool() const { return ptr != nullptr; }

        T* release() {
            T* new_ptr = ptr;
            ptr = nullptr;
            return new_ptr;
        }

        void reset(T* p = nullptr) {
            if (ptr != p) {
                delete ptr;
                ptr = p;
            }
        }

        
        /* Pointer's CORE: with other */
        void swap(UniquePtr& other) {
            T* temp = ptr;
            ptr = other.ptr;
            other.ptr = temp;
        }
};

