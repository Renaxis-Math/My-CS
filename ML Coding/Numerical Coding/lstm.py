"""
Implement Long Short-Term Memory (LSTM) Network
Task: Implement Long Short-Term Memory (LSTM) Network
Your task is to implement an LSTM network that processes a sequence of inputs and produces the final hidden state and cell state after processing all inputs.

Write a class LSTM with the following methods:

__init__(self, input_size, hidden_size): Initializes the LSTM with random weights and zero biases.
forward(self, x, initial_hidden_state, initial_cell_state): Processes a sequence of inputs and returns the hidden states at each time step, as well as the final hidden state and cell state.
The LSTM should compute the forget gate, input gate, candidate cell state, and output gate at each time step to update the hidden state and cell state.

Example
Example:
import numpy as np

input_sequence = np.array([[1.0], [2.0], [3.0]])
initial_hidden_state = np.zeros((1, 1))
initial_cell_state = np.zeros((1, 1))

lstm = LSTM(input_size=1, hidden_size=1)
outputs, final_h, final_c = lstm.forward(input_sequence, initial_hidden_state, initial_cell_state)

print(final_h)

# Expected Output:
# [[0.73698596]] (approximate)
"""

import numpy as np

class LSTM:
    def __init__(self, input_size, hidden_size):
        self.input_size = input_size
        self.hidden_size = hidden_size

        # Initialize weights and biases
        self.Wf = np.random.randn(hidden_size, input_size + hidden_size)
        self.Wi = np.random.randn(hidden_size, input_size + hidden_size)
        self.Wc = np.random.randn(hidden_size, input_size + hidden_size)
        self.Wo = np.random.randn(hidden_size, input_size + hidden_size)

        self.bf = np.zeros((hidden_size, 1))
        self.bi = np.zeros((hidden_size, 1))
        self.bc = np.zeros((hidden_size, 1))
        self.bo = np.zeros((hidden_size, 1))

    def forward(self, x, initial_hidden_state, initial_cell_state):
        h = initial_hidden_state
        c = initial_cell_state
        outputs = []

        for t in range(len(x)):
            xt = x[t].reshape(-1, 1)
            concat = np.vstack((h, xt))

            # Forget gate
            ft = self.sigmoid(np.dot(self.Wf, concat) + self.bf)

            # Input gate
            it = self.sigmoid(np.dot(self.Wi, concat) + self.bi)
            c_tilde = np.tanh(np.dot(self.Wc, concat) + self.bc)

            # Cell state update
            c = ft * c + it * c_tilde

            # Output gate
            ot = self.sigmoid(np.dot(self.Wo, concat) + self.bo)

            # Hidden state update
            h = ot * np.tanh(c)

            outputs.append(h)

        return np.array(outputs), h, c

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
