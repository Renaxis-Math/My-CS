def solve(nums: list[int]) -> int:
    # Time: O(nlogn), n = len(nums)

    # optimal_lis_nums[i] = smallest possible value satisfy LIS length i
    optimal_lis_nums = [float('inf')] * (len(nums) + 1)
    optimal_lis_nums[0] = -float('inf') # IMPORTANT

    # for reconstruction
    parents = [i for i in range(len(nums))]
    per_length_tail_indices = [0] * (len(nums) + 1)

    # for each num (left -> right),
    # find among 'optimal_lis_nums' (since already sorted), which:
    #   - if non-float('inf)    = seen nums
    #   - if float('inf')       = unseen nums
    # the first (which is also the smallest) 'seen-num' >= 'num'
    for i, num in enumerate(nums):
        replace_at_length = _bin_search(
            0, len(optimal_lis_nums) - 1,
            # if optimal_lis_nums[mid_i] >= num
            # 'future optimal_lis_nums' >= num as well
            lambda mid_i: optimal_lis_nums[mid_i] >= num
        )
        
        if replace_at_length:
            optimal_lis_nums[replace_at_length] = num

            if replace_at_length > 1:
                parents[i] = per_length_tail_indices[replace_at_length - 1]

            per_length_tail_indices[replace_at_length] = i


    # as premise, any non-float('inf' or -'inf') is our ans
    answers = [
        num for num in optimal_lis_nums 
        if num not in [float('inf'), -float('inf')]
    ]

    last_lis_index = per_length_tail_indices[len(answers)]
    lis = _reconstruct(parents, last_lis_index, nums)
    print(lis)

    return len(answers)

""" Always setup FF.FT..TT to find first True"""
def _bin_search(start_i, end_i, _in_right_region: "func"):
    # Time: O(log(end_i - start_i + 1) * O(in_right_region))

    # Find within [start_i, end_i], TT..T -> start_i
    left_i, right_i = start_i, end_i

    while left_i <= right_i:
        mid_i = left_i + (right_i - left_i) // 2

        # _in_right_region() always contains the answer
        if _in_right_region(mid_i):
            right_i = mid_i - 1
        else:
            left_i = mid_i + 1 

    # None = FF...F = unfound
    return left_i if start_i <= left_i <= end_i else None

def _reconstruct(parents, last_lis_index, nums):
    answers = [nums[last_lis_index]]
    
    cur_i = last_lis_index
    while cur_i != parents[cur_i]:
        cur_i = parents[cur_i]
        answers.append(nums[cur_i])
    
    answers.reverse()
    return answers
