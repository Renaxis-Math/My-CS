#include<utility>
#include<cassert>
#include<cstddef>   // for size_t

template<typename T>
class SharedPtr {
    T* ptr = nullptr;
    std::size_t* count_ptr = nullptr;

    public:
        constexpr SharedPtr() = default;
        // don't want implicit type conversions since wrappers are independent
        explicit SharedPtr(T* p) : ptr{p} 
        {
            if (p) count_ptr = new std::size_t{1};
        }
        
        /* NEW: extra Helper Function */
        void dereference_if_can() {
            if (count_ptr && --(*count_ptr) == 0) {
                delete ptr; delete count_ptr;
            }
        }

        /* Rule of 3 */

        // Copy allowed, we'll just need to add to Counter
        SharedPtr(const SharedPtr& other) : 
            ptr{other.ptr}, count_ptr{other.count_ptr} 
        {
            if (count_ptr) ++(*count_ptr);
        }
        SharedPtr& operator=(const SharedPtr& other) {
            if (this != &other) {
                dereference_if_can();

                ptr = other.ptr; 
                count_ptr = other.count_ptr;
                if (count_ptr) ++(*count_ptr);
            }
            return *this;
        }
        // Your class owns a resource, so you must explicitly release it
        // -> don't use `= default`: it destroys the SharedPtr object, not the `ptr` field.
        ~SharedPtr() { dereference_if_can(); }


        /* Rule of 5 (3 + 2 add-on) for std::move() */
        
        SharedPtr(SharedPtr&& other) :
            ptr{other.ptr}, count_ptr{other.count_ptr} 
        {
            other.ptr = nullptr; other.count_ptr = nullptr;
        }

        SharedPtr& operator=(SharedPtr&& other) {
            // Even though `other` has type T&&, it's a named variable, 
            // hence, it's an lvalue expression inside the function.
            if (this != &other) {   // avoid self-deletion
                dereference_if_can();
                ptr = other.ptr; count_ptr = other.count_ptr;
                other.ptr = nullptr; other.count_ptr = nullptr;
            }
            return *this;
        }        


        /* Pointer's CORE: itself */
        T* get() const { return ptr; }
        std::size_t get_count() const { return (count_ptr) ? *count_ptr : 0; } /* NEW */

        T& operator*() const { assert(ptr); return *ptr; }
        T* operator->() const { assert(ptr); return ptr; }
        
        // for (!unique_ptr)
        explicit operator bool() const { return ptr != nullptr; }

        T* release() = delete; // shared ownership: raw release breaks counting

        void reset(T* p = nullptr) {
            if (ptr != p) {
                dereference_if_can();
                ptr = p;
                count_ptr = (p) ? new std::size_t(1) : nullptr;
            }
        }
        
        /* Pointer's CORE: with other */
        void swap(SharedPtr& other) {
            std::swap(ptr, other.ptr);
            std::swap(count_ptr, other.count_ptr);
        }
};

