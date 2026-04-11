def solve(nums: list[int]) -> list[int]:
    # Time: O(n^2), n = len(nums)
    
    # answers[i] = length of LIS ending at index i
    answers = [1] * len(nums)

    # for reconstruction: parents[i] = i
    parents = [i for i in range(len(nums))]

    for i in range(len(nums)):
        for prev_i in range(i):
            
            if nums[prev_i] < nums[i]:
                if answers[i] < 1 + answers[prev_i]:
                    answers[i] = 1 + answers[prev_i]

                    parents[i] = prev_i

    last_lis_index = answers.index(max(answers))
    lis = _reconstruct(parents, last_lis_index, nums)
    print(lis)
    return max(answers)

def _reconstruct(parents, last_lis_index, nums):
    answers = [nums[last_lis_index]]
    
    cur_i = last_lis_index
    while cur_i != parents[cur_i]:
        cur_i = parents[cur_i]
        answers.append(nums[cur_i])
    
    answers.reverse()
    return answers
