def solve(nums):
    # We start at 1 because a single item at index 0 is already "sorted"
    for i in range(1, len(nums)):
        unsorted_num = nums[i]

        compare_i = i - 1
        while compare_i >= 0 and nums[compare_i] > unsorted_num:
            # ...shift that bigger card one position to the right
            nums[compare_i + 1] = nums[compare_i]
            compare_i -= 1
        
        # So when the loop stops, there are two possibilities:

        # comparison_index == -1
        # This means card_to_insert is smaller than everything to its left, so it belongs at index 0.
        # elements[comparison_index] <= card_to_insert
        # This means you found the first element that is not bigger, so card_to_insert should go just to the right of it.            
        insert_i = compare_i + 1
        nums[insert_i] = unsorted_num
    
    return nums

elements = [2, 5, 7, 4]
print(solve(elements))