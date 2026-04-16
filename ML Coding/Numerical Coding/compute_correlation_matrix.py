"""
Calculate Correlation Matrix
Write a Python function to calculate the correlation matrix for a given dataset. The function should take in a 2D numpy array X and an optional 2D numpy array Y. If Y is not provided, the function should calculate the correlation matrix of X with itself. It should return the correlation matrix as a 2D numpy array.
Example
Example:
    X = np.array([[1, 2],
                  [3, 4],
                  [5, 6]])
    output = calculate_correlation_matrix(X)
    print(output)
    # Output:
    # [[1. 1.]
    #  [1. 1.]]
    
    Reasoning:
    The function calculates the correlation matrix for the dataset X. In this example, the correlation between the two features is 1, indicating a perfect linear relationship.
    
"""

import numpy as np

def calculate_correlation_matrix(X, Y=None):
    # Helper function to calculate standard deviation
    def calculate_std_dev(A):
        return np.sqrt(np.mean((A - A.mean(0))**2, axis=0))
    
    if Y is None:
        Y = X
    n_samples = np.shape(X)[0]
    # Calculate the covariance matrix
    covariance = (1 / n_samples) * (X - X.mean(0)).T.dot(Y - Y.mean(0))
    # Calculate the standard deviations
    std_dev_X = np.expand_dims(calculate_std_dev(X), 1)
    std_dev_y = np.expand_dims(calculate_std_dev(Y), 1)
    # Calculate the correlation matrix
    correlation_matrix = np.divide(covariance, std_dev_X.dot(std_dev_y.T))

    return np.array(correlation_matrix, dtype=float)
    