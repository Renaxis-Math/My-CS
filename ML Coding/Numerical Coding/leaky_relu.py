"""
Leaky ReLU Activation Function
Write a Python function `leaky_relu` that implements the Leaky Rectified Linear Unit (Leaky ReLU) activation function. The function should take a float `z` as input and an optional float `alpha`, with a default value of 0.01, as the slope for negative inputs. The function should return the value after applying the Leaky ReLU function.
Example
Example:
print(leaky_relu(0)) 
# Output: 0

print(leaky_relu(1)) 
# Output: 1

print(leaky_relu(-1)) 
# Output: -0.01

print(leaky_relu(-2, alpha=0.1))
# Output: -0.2
"""

def leaky_relu(z: float, alpha: float = 0.01) -> float|int:
    return z if z > 0 else alpha * z
