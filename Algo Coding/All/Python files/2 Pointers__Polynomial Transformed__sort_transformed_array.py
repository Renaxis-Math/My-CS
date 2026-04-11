"""
You are given a sorted integer array nums 
and three integer coefficients a, b, and c. 

Your task is to apply a quadratic function 
f(x) = ax² + bx + c to each element in the array 
and return the resulting values in sorted order.
"""

def solve(sorted_nums, a, b, c) -> list:
    """ IDEA:

    If a < 0 -> min is 1 of the edges, increasing as we go center
    If a >= 0 -> max is 1 of the edge, decreasing as we go center
    """
    if not sorted_nums: return []

    from collections import deque
    answers = deque()

    def _f(x): return a*(x**2) + b*x + c

    left_i = 0; right_i = len(sorted_nums) - 1
    while left_i <= right_i:
        left_num = sorted_nums[left_i]
        right_num = sorted_nums[right_i]

        new_left_num = _f(left_num)
        new_right_num = _f(right_num)

        if a > 0:
            if new_left_num > new_right_num:
                answers.appendleft(new_left_num)
                left_i += 1
            else:
                answers.appendleft(new_right_num)
                right_i -= 1
        
        else:
            if new_left_num > new_right_num:
                answers.append(new_right_num)
                right_i -= 1
            else:
                answers.append(new_left_num)
                left_i += 1
    
    return list(answers)

def test():
    nums = [-4, -2, 2, 4]; a = 1; b = 3; c = 5
    assert solve(nums, a, b, c) == [3, 9, 15, 33]

if __name__ == "__main__":
    test()