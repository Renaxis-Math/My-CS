using pii = pair<int, int>;

class LFUCache {
public:
    unordered_map<int, pii> cache; // key -> (val, freq)
    
    // freq -> LinkedList[(key, val)]
    unordered_map<int, list<pii>> freq_map;

    // key -> in freq_map[freq]
    unordered_map<int, list<pii>::iterator> key_node_map;

    int capacity;
    int global_min;

    LFUCache(int capacity) : capacity(capacity), global_min(0) {}
    
    int get(int key) {

        // get the key
        if (!cache.count(key)) return -1;
        auto [val, freq] = cache[key];

        // update old freq_map: erase node, then optionally erase freq
        _remove_old_freq(key, freq);

        // update new freq
        _update_new_freq(key, val, freq + 1);

        return val;
    }

    void _remove_old_freq(int key, int old_freq) {
        auto node = key_node_map[key];
        freq_map[old_freq].erase(node);
        
        if (freq_map[old_freq].empty()) {
            freq_map.erase(old_freq);
            if (global_min == old_freq) global_min++;
        }        
    }

    void _update_new_freq(int key, int val, int new_freq) {
        cache[key] = {val, new_freq};
        freq_map[new_freq].push_front({key, val});
        key_node_map[key] = freq_map[new_freq].begin();
    }
    
    void put(int key, int val) {
        if (!capacity) return;

        if (cache.count(key)) { // If key exists
            cache[key].first = val;
            get(key);
            return;
        }

        if (cache.size() == capacity) {
            // get least recently used node
            auto LFU_LRU_node = freq_map[global_min].back();

            _remove_old_freq(LFU_LRU_node.first, global_min);

            cache.erase(LFU_LRU_node.first);
            key_node_map.erase(LFU_LRU_node.first);
        }

        global_min = 1;
        _update_new_freq(key, val, 1);
    }
};

/**
 * Your LFUCache object will be instantiated and called as such:
 * LFUCache* obj = new LFUCache(capacity);
 * int param_1 = obj->get(key);
 * obj->put(key,value);
 */