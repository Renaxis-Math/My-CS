/* Use when each node can vary # children */

#include <memory>
#include <string>
#include<unordered_map>
using namespace std;

struct Node {
    unordered_map<char, unique_ptr<Node>> children;
    bool is_end = false; // is_end = is end of sentence.

    void add_child(char ch) {
        Node* child = next(ch);
        if (!child) children.emplace(ch, make_unique<Node>());
    }

    Node* next(char ch) {
        return (children.contains(ch)) ? 
            children.at(ch).get() : nullptr;
    }
};

class Trie {
    Node root;

    public:
        Trie() {}

        Node* get_root() { return &root; }

        void insert(string& sentence, int insert_count) {
            // update trie properties here

            // update trie
            Node* cur = get_root();
            for (char ch : sentence) {
                cur->add_child(ch);
                cur = cur->next(ch);

                // update node property here
            }
            cur->is_end = true;
        }
};
