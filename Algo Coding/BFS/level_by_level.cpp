"""
Word Ladder II
LeetCode 126 - Difficulty: Hard

A transformation sequence from word 'beginWord' to word 'endWord' using a dictionary 'wordList' is a sequence of words 'beginWord -> s_1 -> s_2 -> ... -> s_k' such that:

• Every adjacent pair of words differs by a single letter.

• Every 's_i' for '1 <= i <= k' is in 'wordList'. Note that 'beginWord' does not need to be in 'wordList'.

• 's_k == endWord'

Given two words, 'beginWord' and 'endWord', and a dictionary 'wordList', return all the shortest transformation sequences from 'beginWord' to 'endWord', or an empty list if no such sequence exists. Each sequence should be returned as a list of the words '[beginWord, s_1, s_2, ..., s_k]'.



Constraints:

• '1 <= beginWord.length <= 5'

• 'endWord.length == beginWord.length'

• '1 <= wordList.length <= 500'

• 'wordList[i].length == beginWord.length'

• 'beginWord', 'endWord', and 'wordList[i]' consist of lowercase English letters.

• 'beginWord != endWord'

• All the words in 'wordList' are unique.

• The sum of all shortest transformation sequences does not exceed '10^5'.
"""
#include<bits/stdc++.h>
using namespace std;

using vs = vector<string>;

pair<unordered_map<string, vs>, int> _bfs(
    string& begin_word, string& end_word, unordered_set<string>& words_set
);

vs _get_neighbors(string word, unordered_set<string>& words_set);

vector<vector<string>> solve(
    string begin_word, string end_word, vector<string>& wordList) {

    unordered_set<string> words_set(wordList.begin(), wordList.end());
    if (!words_set.contains(end_word)) return {};

    auto [parents_graph, shortest_depth] = 
        _bfs(begin_word, end_word, words_set);

    if (shortest_depth == -1) return {};

    vector<vs> answers;

    // dfs from end depth to 0
    auto reverse_dfs = [&](
        auto&& reverse_dfs, 
        string& word, vs& path, int remain_depth) -> void {

        // base case
        if (remain_depth == 0) {
            if (word == begin_word) {
                vs reversed_path{path.rbegin(), path.rend()};
                answers.emplace_back(reversed_path);
            }
            return;
        }

        for (auto& next_word : parents_graph[word]) {
            path.emplace_back(next_word);
            reverse_dfs(reverse_dfs, next_word, path, remain_depth - 1);
            path.pop_back();
        }
    };

    vs path{end_word};
    reverse_dfs(reverse_dfs, end_word, path, shortest_depth);
    return answers;
}
};

pair<unordered_map<string, vs>, int> _bfs(
    string& begin_word, string& end_word, unordered_set<string>& words_set
) {
    unordered_map<string, vs> parents_graph;
    
    deque<string> queue;
    unordered_set<string> visited;

    queue.emplace_back(begin_word);
    visited.insert(begin_word);

    int depth = 0; bool found_end_word = false;
    while (!queue.empty()) {
        if (found_end_word) break;

        // avoid multi-parent
        unordered_set<string> level_visited;

        int level_size = queue.size();
        for (int _ = 0; _ < level_size; ++_) {
            string word = queue.front(); queue.pop_front();

            vs neighbors = _get_neighbors(word, words_set);

            for (auto& next_word : neighbors) {
                if (next_word == end_word) found_end_word = true;

                if (visited.contains(next_word)) continue;

                parents_graph[next_word].emplace_back(word);
                if (!level_visited.contains(next_word)) {
                    level_visited.insert(next_word);
                    queue.emplace_back(next_word);
                }
            }
        }

        for (auto& word : level_visited) visited.insert(word);
        depth++;
    }

    return {parents_graph, found_end_word ? depth : -1};
}

vs _get_neighbors(string word, unordered_set<string>& words_set) {
    vs answers;
    for (int i = 0; i < word.size(); ++i) {
        char old_char = word[i];
        for (char new_char = 'a'; new_char <= 'z'; ++new_char) {
            if (new_char == old_char) continue;
            word[i] = new_char;
            if (words_set.contains(word)) answers.emplace_back(word);
        }
        word[i] = old_char;
    }
    return answers;
}