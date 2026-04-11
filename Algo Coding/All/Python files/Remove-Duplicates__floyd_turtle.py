""" Requirements
1. num in [1...n-1]
2. arr has exactly 1 dup.
3. that dup. appears exactly 2 times
"""

def solve(nums):
    if not nums: return []

    # Phase 1: find a random spot in the cycle
    # with fast and slow pointer
    fast_i, slow_i = nums[0], nums[0]

    while True:
        slow_i = nums[slow_i]
        fast_i = nums[nums[fast_i]]

        if fast_i == slow_i: break
    
    # Phase 2: find entry to cycle, which's our ans
    p1 = nums[0]; p2 = slow_i
    while p1 != p2:
        p1 = nums[p1]
        p2 = nums[p2]
    
    return p1