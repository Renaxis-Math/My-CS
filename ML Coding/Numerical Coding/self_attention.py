"""
Implement Self-Attention Mechanism
Task: Implement the Self-Attention Mechanism
Your task is to implement the self-attention mechanism, which is a fundamental component of transformer models, widely used in natural language processing and computer vision tasks. The self-attention mechanism allows a model to dynamically focus on different parts of the input sequence when generating a contextualized representation.

Your function should return the self-attention output as a numpy array.

Example
Example:
import numpy as np

X = np.array([[1, 0], [0, 1]])
W_q = np.array([[1, 0], [0, 1]])
W_k = np.array([[1, 0], [0, 1]])
W_v = np.array([[1, 2], [3, 4]])

Q, K, V = compute_qkv(X, W_q, W_k, W_v)
output = self_attention(Q, K, V)

print(output)

# Expected Output:
# [[1.660477 2.660477]
#  [2.339523 3.339523]]
"""

import numpy as np

def compute_qkv(X, W_q, W_k, W_v):
    Q = np.dot(X, W_q)
    K = np.dot(X, W_k)
    V = np.dot(X, W_v)
    return Q, K, V

def self_attention(Q, K, V):
    d_k = Q.shape[1]
    scores = np.matmul(Q, K.T) / np.sqrt(d_k)
    attention_weights = np.exp(scores) / np.sum(np.exp(scores), axis=1, keepdims=True)
    attention_output = np.matmul(attention_weights, V)
    return attention_output

