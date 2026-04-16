"""
Implement Lasso Regression using Gradient Descent
In this problem, you need to implement the Lasso Regression algorithm using Gradient Descent. Lasso Regression (L1 Regularization) adds a penalty equal to the absolute value of the coefficients to the loss function. Your task is to update the weights and bias iteratively using the gradient of the loss function and the L1 penalty.

Your task is to use the L1 penalty to shrink some of the feature coefficients to zero during gradient descent, thereby helping with feature selection.

Example:
import numpy as np

X = np.array([[0, 0], [1, 1], [2, 2]])
y = np.array([0, 1, 2])

alpha = 0.1
weights, bias = l1_regularization_gradient_descent(X, y, alpha=alpha, learning_rate=0.01, max_iter=1000)

# Expected Output:
(weights,bias)
(array([float, float]), float)
"""

import numpy as np

def l1_regularization_gradient_descent(X: np.array, y: np.array, alpha: float = 0.1, learning_rate: float = 0.01, max_iter: int = 1000, tol: float = 1e-4) -> tuple:
    n_samples, n_features = X.shape
    # Zero out weights and bias
    weights = np.zeros(n_features)
    bias = 0
    
    for iteration in range(max_iter):
        # Predict values
        y_pred = np.dot(X, weights) + bias
        # Calculate error
        error = y_pred - y
        # Gradient for weights with L1 penalty
        grad_w = (1 / n_samples) * np.dot(X.T, error) + alpha * np.sign(weights)
        # Gradient for bias (no penalty for bias)
        grad_b = (1 / n_samples) * np.sum(error)
        
        # Update weights and bias
        weights -= learning_rate * grad_w
        bias -= learning_rate * grad_b
        
        # Check for convergence
        if np.linalg.norm(grad_w, ord=1) < tol:
            break
    
    return weights, bias
