"""
Word Search
LeetCode 79 - Difficulty: Medium

Given an 'm x n' grid of characters 'board' and a string 'word', return 'true' if 'word' exists in the grid.

The word can be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once.



Constraints:

• 'm == board.length'

• 'n = board[i].length'

• '1 <= m, n <= 6'

• '1 <= word.length <= 15'

• 'board' and 'word' consists of only lowercase and uppercase English letters.



Follow up: Could you use search pruning to make your solution faster with a larger 'board'?
"""

#include<vector>
#include<array>
#include<vector>
#include<unordered_map>
using namespace std;

using pii = pair<int, int>;
constexpr array<pii, 4> DIRS{{
    {0, 1}, {0, -1}, {1, 0}, {-1, 0}
}};

bool solve(vector<vector<char>>& board, string word) {
    int n_row = board.size(), n_col = board[0].size();

    // build frequency maps
    unordered_map<char, int> board_freq, word_freq;
    for (int r = 0; r < n_row; ++r) {
        for (int c = 0; c < n_col; ++c) {
            board_freq[board[r][c]]++;
        }
    }
    for (int i = 0; i < word.size(); ++i) word_freq[word[i]]++;

    // early pruning: pick fewer frequency starting char
    if (board_freq[word[0]] > word_freq[word.back()]) reverse(word.begin(), word.end());
    
    // dfs
    auto dfs = [&](
        auto&& dfs,
        int r, int c, int i,
        vector<vector<bool>>& memo
    ) -> bool { // i = word_i
        if (i == word.size() - 1) return true;
        
        // early pruning: if # next char on board < # next char required
        if (board_freq[board[r][c]] < word_freq[word[i]]) return false;

        for (auto& [dr, dc] : DIRS) {
            int nr = r + dr, nc = c + dc, ni = i + 1;

            if (!(0 <= nr && nr < n_row && 0 <= nc && nc < n_col)) continue;
            if (board[nr][nc] != word[ni]) continue;

            if (!memo[nr][nc]) {
                memo[nr][nc] = true;
                if (dfs(dfs, nr, nc, ni, memo)) return true;
                memo[nr][nc] = false;
            }
        }

        return false;
    };

    vector<vector<bool>> memo(n_row, vector<bool>(n_col, false));
    
    for (int r = 0; r < n_row; ++r) {
        for (int c = 0; c < n_col; ++c) {
            if (board[r][c] == word[0]) {
                memo[r][c] = true;
                if (dfs(dfs, r, c, 0, memo)) return true;
                memo[r][c] = false;
            }
        }
    }

    return false;
}