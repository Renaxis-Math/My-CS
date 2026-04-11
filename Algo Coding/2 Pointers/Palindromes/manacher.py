"""
Palindromic Substrings
LeetCode 647 - Difficulty: Medium

Given a string 's', return the number of palindromic substrings in it.

A string is a palindrome when it reads the same backward as forward.

A substring is a contiguous sequence of characters within the string.



Constraints:

• '1 <= s.length <= 1000'

• 's' consists of lowercase English letters.
"""

def solve(string):
    oddString_can_skips = _get_answers_manacher(string, False)
    evenString_can_skips = _get_answers_manacher(string, True)

    # singles + all longer odd palindromes + all even palindromes
    return len(string) + sum(oddString_can_skips) + sum(evenString_can_skips)

def _get_answers_manacher(s, is_even = False):

    # center and right boundary of current rightmost palindrome
    optimal_center_i = 0
    optimal_right_i = -1

    # canSkip_counts for each right_center_i, from right_center_i to optimal_right_i
    answers = [0] * len(s)

    for right_center_i in range(len(s)):

        # if right_center_i is withinn the right-most palindrome, 
        # find its mirrored left_center_i and update can_skips        
        if right_center_i <= optimal_right_i:
            # 2 * [... opt_c_i] - ([... opt_c_i] + [opt_c_i ... r_c_i])
            left_center_i = 2 * optimal_center_i - right_center_i + (1 if is_even else 0)

            answers[right_center_i] = min(
                answers[left_center_i],
                optimal_right_i - right_center_i + 1
            )

        # try to update can_skips BEYOND optimal_right_i
        while True:
            new_one_sided_length = answers[right_center_i] + 1
            new_left_i = right_center_i - new_one_sided_length
            new_right_i = right_center_i + new_one_sided_length - (1 if is_even else 0)

            if new_left_i < 0 or new_right_i >= len(s): break
            if s[new_left_i] != s[new_right_i]: break

            answers[right_center_i] += 1

            if new_right_i > optimal_right_i:
                optimal_right_i = new_right_i
                optimal_center_i = right_center_i

    return answers
