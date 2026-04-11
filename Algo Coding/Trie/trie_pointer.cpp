struct Node {
    unordered_map<char, unique_ptr<Node>> children;
    bool is_end = false; // is_end = is end of sentence.

    void add_child(const char& ch) {
        Node* child = next(ch);
        if (!child) children.emplace(ch, make_unique<Node>());
    }

    Node* next(const char& ch) {
        return (children.contains(ch)) ? 
            children.at(ch).get() : nullptr;
    }
};

class Trie {
    Node root;

    public:
        Trie() {}

        Node* get_root() { return &root; }

        void insert(const string& branch) { // or string branch
            // update trie properties here

            // update trie
            Node* cur_node = get_root();
            for (char ch : branch) {
                cur_node->add_child(ch);
                cur_node = cur_node->next(ch);

                // update node property here
            }
            cur_node->is_end = true;
        }
    
        bool search(const string& word) {
            Node* node = _traverse(word);
            return node && node->is_end;
        }
    
        bool startsWith(const string& prefix) {
            Node* node = _traverse(prefix);
            return node != nullptr;
        }

        Node* _traverse(const string& branch) {
            Node* cur_node = get_root();
            int i = 0;
            while (cur_node && i < branch.size()) {
                cur_node = cur_node->next(branch[i]);
                i++;
            }
            return cur_node;
        }
};

/**
 * Your Trie object will be instantiated and called as such:
 * Trie* obj = new Trie();
 * obj->insert(word);
 * bool param_2 = obj->search(word);
 * bool param_3 = obj->startsWith(prefix);
 */