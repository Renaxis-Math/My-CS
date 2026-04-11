/* Goal: Time complexity: O(1) amortized; Space Complexity: O(n)
*/

#include<vector>
#include<unordered_map>
using namespace std;

#include<cstddef>
#include<cstdlib>

class RandomizedSet {
    vector<int> nums;
    unordered_map<int, size_t> num_index_map;

public:
    RandomizedSet() {}
    
    bool insert(int val) {
        if (num_index_map.count(val)) return false;

        nums.push_back(val);
        num_index_map[val] = nums.size() - 1;

        return not_exist;
    }
    
    bool remove(int val) {
        if (!num_index_map.count(val)) return false;

        // swap and update
        size_t index = num_index_map.at(val);
        num_index_map[nums.back()] = index;

        swap(nums[index], nums.back());
        

        // remove
        nums.pop_back();
        num_index_map.erase(val);

        return true;
    }
    
    int getRandom() {
        size_t random_index = rand() % nums.size();
        return nums[random_index];
    }
};

/**
 * Your RandomizedSet object will be instantiated and called as such:
 * RandomizedSet* obj = new RandomizedSet();
 * bool param_1 = obj->insert(val);
 * bool param_2 = obj->remove(val);
 * int param_3 = obj->getRandom();
 */