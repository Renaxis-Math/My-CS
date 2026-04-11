#include<vector>
#include<deque>
using namespace std;

struct TreeNode {
    int val; TreeNode *left; TreeNode *right;
    TreeNode(int x = 0, TreeNode *left = nullptr, TreeNode *right = nullptr) :
        val(x), left(left), right(right)
    {}
};

using Node = TreeNode;

vector<vector<int>> solve(Node* root) {
    vector<vector<int>> answers;
    if (!root) return answers;
    
    deque<Node*> q{root}; bool is_left_to_right = true;
    while (!q.empty()) {

        vector<int> level_nodes(q.size());

        for (int i = 0; i < level_nodes.size(); ++i) {

            Node* node = q.front(); q.pop_front();

            int insert_i = is_left_to_right ? i : level_nodes.size()-1 - i;
            level_nodes[insert_i] = node->val;

            if (node->left) q.push_back(node->left);
            if (node->right) q.push_back(node->right);
        }

        answers.push_back(level_nodes);
        is_left_to_right = !is_left_to_right;
    }
    
    return answers;
}