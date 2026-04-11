template <typename T, typename... Args>
T max_of(T first, Args... args) {
    T ans = first;
    ( (ans = max(ans, args)), ... );
    return ans;
}

int solve(TreeNode* root) {
    int final_ans = numeric_limits<int>::min();

    auto dfs = [&](auto&& dfs, TreeNode* node) -> int {
        if (!node) return numeric_limits<int>::min();

        int left_ans = dfs(dfs, node->left);
        int right_ans = dfs(dfs, node->right);

        int local_ans =
            node->val + max_of(0, left_ans, right_ans);

        final_ans = max_of(final_ans,
            local_ans,
            left_ans, right_ans,
            node->val + max(0, left_ans) 
            + max(0, right_ans)
        );

        return local_ans;
    };

    dfs(dfs, root);
    return final_ans;
}