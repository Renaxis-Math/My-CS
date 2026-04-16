"""
2D Translation Matrix Implementation
Task: Implement a 2D Translation Matrix
Your task is to implement a function that applies a 2D translation matrix to a set of points. A translation matrix is used to move points in 2D space by a specified distance in the x and y directions.

Write a function translate_object(points, tx, ty) where points is a list of [x, y] coordinates and tx and ty are the translation distances in the x and y directions respectively.

The function should return a new list of points after applying the translation matrix.

Example
Example:
import numpy as np

points = [[0, 0], [1, 0], [0.5, 1]]
tx, ty = 2, 3

print(translate_object(points, tx, ty))

# Expected Output:
# [[2.0, 3.0], [3.0, 3.0], [2.5, 4.0]]
"""

import numpy as np

def translate_object(points, tx, ty):
    translation_matrix = np.array([
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ])
    
    homogeneous_points = np.hstack([np.array(points), np.ones((len(points), 1))])
    
    translated_points = np.dot(homogeneous_points, translation_matrix.T)
    
    return translated_points[:, :2].tolist()
