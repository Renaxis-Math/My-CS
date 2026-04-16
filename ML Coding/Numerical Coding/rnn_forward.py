"""
Implementing a Simple RNN
Write a Python function that implements a simple Recurrent Neural Network (RNN) cell. The function should process a sequence of input vectors and produce the final hidden state. Use the tanh activation function for the hidden state updates. The function should take as inputs the sequence of input vectors, the initial hidden state, the weight matrices for input-to-hidden and hidden-to-hidden connections, and the bias vector. The function should return the final hidden state after processing the entire sequence, rounded to four decimal places.
Example
Example:
    input_sequence = [[1.0], [2.0], [3.0]]
    initial_hidden_state = [0.0]
    Wx = [[0.5]]  # Input to hidden weights
    Wh = [[0.8]]  # Hidden to hidden weights
    b = [0.0]     # Bias
    output: final_hidden_state = [0.9993]
    reasoning: The RNN processes each input in the sequence, upda
"""

import numpy as np

def rnn_forward(input_sequence, initial_hidden_state, Wx, Wh, b):
    h = np.array(initial_hidden_state)
    Wx = np.array(Wx)
    Wh = np.array(Wh)
    b = np.array(b)
    for x in input_sequence:
        x = np.array(x)
        h = np.tanh(np.dot(Wx, x) + np.dot(Wh, h) + b)
    final_hidden_state = np.round(h, 4)
    return final_hidden_state.tolist()
