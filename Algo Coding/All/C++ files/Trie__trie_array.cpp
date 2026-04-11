/* Use when nodes have fixed size: use indices, no pointers. */

#include <array>
#include <string>
#include <vector>

using namespace std;

struct Node {
    // index 0 = root, index > 0 = children
    array<int, 26> children;
    bool is_prefix_end = false;
};

class Trie {
    // Node root;
    vector<Node> tree;

public:
    Trie(){ tree.push_back(Node{}); }
   
    void insert(string word) {
        int cur_i = 0; // root

        // insert a branch
        for (int i = 0; i < word.size(); ++i) {
            int char_i = word[i] - 'a';
    
            // non-root can't point 0 (root) -> this means None
            if (tree[cur_i].children[char_i] == 0) {
                tree[cur_i].children[char_i] = tree.size();
                tree.push_back(Node{}); // NEW
            }

            cur_i = tree[cur_i].children[char_i];

            // set end_of_branch for leaf
            if (i == word.size() - 1)
                tree[cur_i].is_prefix_end = true;
        }
    }

    int _traverse(string& branch) {
        int cur_i = 0;
        
        for (char ch : branch) {
            cur_i = tree[cur_i].children[ch - 'a'];
            if (!cur_i) break; // 0
        }
        return cur_i;
    }
    
    bool search(string word) {
        int cur_i = _traverse(word);
        return (cur_i && tree[cur_i].is_prefix_end);
    }
    
    bool startsWith(string prefix) {
        int cur_i = _traverse(prefix);
        return cur_i != 0;
    }
};
