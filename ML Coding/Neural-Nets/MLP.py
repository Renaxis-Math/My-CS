import torch
from torch import nn

class MLP(nn.Module):
    def __init__(
        self,
        input_layer_size,
        hidden_layer_sizes: list[int], # n_layer = len(hidden_layer_sizes)
        output_layer_size = 1,
        activation_func = nn.ReLU
    ):
        super().__init__()
        
        self.hidden_layers = nn.Sequential(
            *self._build_hidden_layers(
                input_layer_size,
                hidden_layer_sizes,
                activation_func
            )
        )

        # Connect to output layer
        last_hidden_size = hidden_layer_sizes[-1] if len(hidden_layer_sizes) > 0 else input_layer_size
        self.output_layer = nn.Linear(last_hidden_size, output_layer_size)

    def _build_hidden_layers(self, 
        input_layer_size, 
        hidden_layer_sizes: list[int],
        activation_func
    ) -> list[nn.Module]:
        answers = []
        
        # Build hidden layers
        cur_layer_size = input_layer_size
        for hidden_layer_size in hidden_layer_sizes:
            answers.append(nn.Linear(cur_layer_size, hidden_layer_size))
            answers.append(activation_func()) # must be independent object

            # Update
            cur_layer_size = hidden_layer_size
        
        return answers

    # A must-have
    def forward(self, X: torch.Tensor) -> torch.Tensor:
        # X shape = (batch_size, input_layer_size)
        hidden_values = self.hidden_layers(X)

        # predictions shape = (batch_size, output_layer_size)
        predictions = self.output_layer(hidden_values)
        return predictions