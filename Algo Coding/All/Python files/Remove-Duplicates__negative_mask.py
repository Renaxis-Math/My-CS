def find_duplicates_negative_marking(nums):
    """
    nums[i] must be in [0, len(nums)-1].
    
    Modifies nums (but we restore it at the end).
    Returns all duplicates.
    """
    dups = []
    for i in range(len(nums)):
        idx = abs(nums[i])

        if nums[idx] < 0: # DUPLICATE FOUND
            dups.append(idx)
        else:
            nums[idx] = -nums[idx]

    # optional: restore
    for i in range(len(nums)):
        nums[i] = abs(nums[i])

    return dups