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

    # None = FF...F = unfound, can remove the condition (just return left_i) if needed
    return left_i if start_i <= left_i <= end_i else None