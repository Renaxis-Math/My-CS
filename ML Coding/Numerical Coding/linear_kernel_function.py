"""
Linear Kernel Function
Write a Python function `kernel_function` that computes the linear kernel between two input vectors `x1` and `x2`. The linear kernel is defined as the dot product (inner product) of two vectors.
Example
Example:
import numpy as np

x1 = np.array([1, 2, 3])
x2 = np.array([4, 5, 6])

result = kernel_function(x1, x2)
print(result)
# Expected Output: 32
"""

import numpy as np

def kernel_function(x1, x2):
    return np.inner(x1, x2)
