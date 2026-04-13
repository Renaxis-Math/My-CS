#ifndef SHARED_GET_NAME_H
#define SHARED_GET_NAME_H

class SharedGetName {
    const char* _name;

    public:
        explicit SharedGetName(const char* name) :
            _name{name}
        {}

        const char* get_name() const {
            return _name;
        }
};

#endif
