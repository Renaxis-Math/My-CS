def solve(nums: list[int]) -> int:        
    ans = None
    majority_count = 0

    for num in nums:
        if majority_count == 0:
            ans = num
            majority_count += 1
        
        else:
            if num == ans:
                majority_count += 1
            else:
                majority_count -= 1
    
    return ans
