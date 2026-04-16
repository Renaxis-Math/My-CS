"""
Implement Reduced Row Echelon Form (RREF) Function
In this problem, your task is to implement a function that converts a given matrix into its Reduced Row Echelon Form (RREF). The RREF of a matrix is a special form where each leading entry in a row is 1, and all other elements in the column containing the leading 1 are zeros, except for the leading 1 itself.

However, there are some additional details to keep in mind:

Diagonal entries can be 0 if the matrix is reducible (i.e., the row corresponding to that position can be eliminated entirely).
Some rows may consist entirely of zeros.
If a column contains a pivot (a leading 1), all other entries in that column should be zero.
Your task is to implement the RREF algorithm, which must handle these cases, and convert any given matrix into its RREF.

Example
Example:
import numpy as np

matrix = np.array([
    [1, 2, -1, -4],
    [2, 3, -1, -11],
    [-2, 0, -3, 22]
])

rref_matrix = rref(matrix)
print(rref_matrix)

# Expected Output:
# array([
#    [ 1.  0.  0. -8.],
#    [ 0.  1.  0.  1.],
#    [-0. -0.  1. -2.]
# ])
"""

import numpy as np

def rref(matrix):
    # Convert to float for division operations
    A = matrix.astype(np.float32)
    n, m = A.shape
    
    for i in range(n):
        if A[i, i] == 0:
            nonzero_rel_id = np.nonzero(A[i:, i])[0]
            if len(nonzero_rel_id) == 0: continue
            
            A[i] = A[i] + A[nonzero_rel_id[0] + i]

        A[i] = A[i] / A[i, i]
        for j in range(n):
            if i != j:
                A[j] -= A[j, i] * A[i]

    return A
