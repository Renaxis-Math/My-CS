"""
Given an array arr[] containing n integers. The problem is to count the number of increasing subsequences in the array of size k.

Examples:

Input : arr[] = {2, 6, 4, 5, 7}, k = 3
Output: 5
The subsequences of size 3 are: {2, 6, 7}, {2, 4, 5}, {2, 4, 7}, {2, 5, 7} and {4, 5, 7}.

Input : arr[] = {12, 8, 11, 13, 10, 15, 14, 16, 20}, k = 4
"""

# First Solution: DP. O(len(nums) * K * len(nums)) time
def solve(nums: list[int], K: int):    
    """ IDEA: DP

    answers[k][i] = # increasing subsequence length k <= K of nums[0...i]

    Base:
    
    k = 0:
    answers[0][i] = 0

    k = 1
    answers[1][i] = 1

    i = 0: already covered

    Normal case (Recurrence):

    - nums[i] > nums[prev_i] for all 0 <= prev_i <= i-1:
        answers[k][i] += answers[k-1][prev_i]

    Range:
    k: 0 -> K
    i: 0 -> len(nums) - 1

    Original answer: sum(answers[k])
    """
    if K < 0 or not nums: return 0

    answers = [[0 for i in range(len(nums))] for k in range(K+1)]

    for k in range(0, K+1):
        for i in range(0, len(nums)):
            dp_k = k; dp_i = i          # since range of k, i matches array index

            ans = answers[dp_k][dp_i]   # always use dp_{} to access 'answers'

            # Base case
            if k == 0:
                ans = 0
            elif k == 1:
                ans = 1
            
            # Normal
            else:
                for prev_i in range(i):
                    ans += answers[k-1][prev_i] if nums[i] > nums[prev_i] else 0

            answers[dp_k][dp_i] = ans
    
    final_ans = sum(answers[k])
    return final_ans

# Optimal Solution: Segment Tree
def solve_follow_up_optimal(nums, K):
    """ IDEA:

    1. Since DP has: 
    
    Normal case (Recurrence):

    - nums[i] > nums[prev_i] for all 0 <= prev_i <= i-1:
        answers[k][i] += answers[k-1][prev_i]    

    -> For each i (nums[i]):
        1. we want the sum of an array answers[k-1],
        where each index = a rank mapped from value nums[prev_i] < nums[i]

        2. we want access the segment tree of (k-1)
    
        3. That sum is O(n), but we can break down to O(log n)
        to trade O(log n) insert to segment tree

    2. To handle negative number (segment tree = array index),
    we map each value to:
        1: a rank >= 0
        2: in ascending order

    3. To handle duplicates, we use sorted(nums)

    """
    
    # NEW
    sorted_unique_nums = sorted(set(nums))
    num_rank_map = {num: i for i, num in enumerate(sorted_unique_nums)}

    from segment_tree import SegTree
    k_seg_trees = [SegTree(len(num_rank_map)) for _ in range(K+1)]
    # END NEW

    answers = [[0 for i in range(len(nums))] for k in range(K+1)]

    for k in range(0, K+1):

        for i in range(0, len(nums)):
            dp_k = k; dp_i = i          # since range of k, i matches array index

            ans = answers[dp_k][dp_i]   # always use dp_{} to access 'answers'

            # Base case
            if k == 0:
                ans = 0
            elif k == 1:
                ans = 1
            
            # Normal
            else:

                # for prev_i in range(i):
                #     ans += answers[k-1][prev_i] if nums[i] > nums[prev_i] else 0
                
                # NEW
                rank = num_rank_map[nums[i]]
                seg = k_seg_trees[k-1]
                
                ans += seg.query(0, rank - 1)
                seg.update(rank, answers[k-1][i])
                # END NEW
            
            answers[dp_k][dp_i] = ans
    
    final_ans = sum(answers[k])
    return final_ans

def test():
    assert solve([2, 6, 4, 5, 7], 3) == 5
    assert solve([2, 6, 4, 5, 7], 3) == solve_follow_up_optimal([2, 6, 4, 5, 7], 3)

if __name__ == "__main__":
    test()