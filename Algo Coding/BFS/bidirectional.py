"""
Word Ladder
LeetCode 127 - Difficulty: Hard

A transformation sequence from word 'beginWord' to word 'endWord' using a dictionary 'wordList' is a sequence of words 'beginWord -> s_1 -> s_2 -> ... -> s_k' such that:

• Every adjacent pair of words differs by a single letter.

• Every 's_i' for '1 <= i <= k' is in 'wordList'. Note that 'beginWord' does not need to be in 'wordList'.

• 's_k == endWord'

Given two words, 'beginWord' and 'endWord', and a dictionary 'wordList', return the number of words in the shortest transformation sequence from 'beginWord' to 'endWord', or '0' if no such sequence exists.



Constraints:

• '1 <= beginWord.length <= 10'

• 'endWord.length == beginWord.length'

• '1 <= wordList.length <= 5000'

• 'wordList[i].length == beginWord.length'

• 'beginWord', 'endWord', and 'wordList[i]' consist of lowercase English letters.

• 'beginWord != endWord'

• All the words in 'wordList' are unique.
"""

from collections import deque

def solve(beginWord, endWord, wordList):
    wordSet = set(wordList)
    if endWord not in wordSet: return 0

    def get_neighbors(word):
        for i in range(len(word)):
            for char_i in range(26):
                ch = chr(char_i + ord('a'))
                if ch == word[i]:
                    continue
                next_word = word[:i] + ch + word[i + 1:]
                if next_word in wordSet:
                    yield next_word

    q1 = deque([beginWord])
    q2 = deque([endWord])

    visited1 = {beginWord: 1}   # number of words in path so far
    visited2 = {endWord: 1}

    return 1 + _bfs_bidrectional(q1, q2, visited1, visited2, get_neighbors) 

def _bfs_bidrectional(
    q1: deque, q2: deque,
    visited1: dict, visited2: dict, 
    get_neighbors: "func") -> int:

    for root in q1:
        visited1[root] = 0 # root -> depth
    for root in q2:
        visited2[root] = 0

    while q1 and q2:

        # choose which side to expand this round (smaller frontier)
        if len(q1) <= len(q2):
            small_q, big_q = q1, q2
            small_visited, big_visited = visited1, visited2
        else:
            small_q, big_q = q2, q1
            small_visited, big_visited = visited2, visited1

        min_edge_count = float('inf')

        # IMPORTANT: process the whole level before returning.
        # Early-return on the first overlap can be wrong in bidirectional BFS.
        for _ in range(len(small_q)):   # one BFS level
            node = small_q.popleft()

            for next_node in get_neighbors(node):
                if next_node in small_visited:
                    continue

                # NEW
                if next_node in big_visited:   # searches meet
                    edge_count = small_visited[node] + big_visited[next_node] + 1

                    min_edge_count = min(min_edge_count, edge_count)
                    continue
                else:
                # END NEW
                    small_visited[next_node] = small_visited[node] + 1
                    small_q.append(next_node)

        if min_edge_count < float('inf'):
            return min_edge_count

    return -1