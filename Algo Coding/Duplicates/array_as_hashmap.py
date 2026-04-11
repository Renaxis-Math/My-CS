def find_duplicates_array_hashmap_iter(nums):
    """
    nums has length n, values in [1, n-1].
    Reorders nums so that value v ideally sits at index v-1.
    Any value that can't sit correctly is a duplicate.
    Returns ALL duplicates.
    """
    i = 0
    while i < len(nums):
        correct_i = nums[i] - 1
        if nums[i] != nums[correct_i]:
            nums[i], nums[correct_i] = nums[correct_i], nums[i]
        else:
            i += 1

    dups = []
    for i, v in enumerate(nums):
        if v != i + 1: # DUPLICATE FOUND
            dups.append(v)
    return dups