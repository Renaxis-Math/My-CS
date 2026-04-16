"""
Simple Convolutional 2D Layer
In this problem, you need to implement a 2D convolutional layer in Python. This function will process an input matrix using a specified convolutional kernel, padding, and stride.

Example
Example:
import numpy as np
input_matrix = np.array([
    [1., 2., 3., 4., 5.],
    [6., 7., 8., 9., 10.],
    [11., 12., 13., 14., 15.],
    [16., 17., 18., 19., 20.],
    [21., 22., 23., 24., 25.],
])
kernel = np.array([
    [1., 2.],
    [3., -1.],
])
padding, stride = 0, 1
# Expected Output:
np.array([
    [ 16., 21., 26., 31.],
    [ 41., 46., 51., 56.],
    [ 66., 71., 76., 81.],
    [ 91., 96., 101., 106.],
])
"""

import numpy as np

def simple_conv2d(input_matrix: np.ndarray, kernel: np.ndarray, padding: int, stride: int):
    input_height, input_width = input_matrix.shape
    kernel_height, kernel_width = kernel.shape

    padded_input = np.pad(input_matrix, ((padding, padding), (padding, padding)), mode='constant')
    input_height_padded, input_width_padded = padded_input.shape

    output_height = (input_height_padded - kernel_height) // stride + 1
    output_width = (input_width_padded - kernel_width) // stride + 1

    output_matrix = np.zeros((output_height, output_width))

    for i in range(output_height):
        for j in range(output_width):
            region = padded_input[i*stride:i*stride + kernel_height, j*stride:j*stride + kernel_width]
            output_matrix[i, j] = np.sum(region * kernel)

    return output_matrix
