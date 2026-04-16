import torch
from torch import nn

class RecurrentNN(nn.Module):
    def __init__(
        self,
        input_layer_size: int,
        hidden_layer_sizes: list[int],  # # layers = len(hidden_layer_sizes)
        output_layer_size: int = 1,

        # NEW
        model = nn.RNN,                 # or nn.LSTM
        use_bidirectional: bool = False
    ):
        super().__init__()
        self.model = model
        self.direction_count = 2 if use_bidirectional else 1

        self.hidden_layers = nn.ModuleList(
            self._build_hidden_layers(
                input_layer_size,
                hidden_layer_sizes,
                use_bidirectional
            )
        )

        last_hidden_size = hidden_layer_sizes[-1] if hidden_layer_sizes else input_layer_size
        self.output_layer = nn.Linear(last_hidden_size * self.direction_count, output_layer_size)

    def _build_hidden_layers(
        self,
        input_layer_size: int,
        hidden_layer_sizes: list[int],
        use_bidirectional: bool
    ) -> list[nn.Module]:

        answers = []

        cur_layer_size = input_layer_size
        for hidden_layer_size in hidden_layer_sizes:
            answers.append(
                self.model(
                    cur_layer_size,
                    hidden_layer_size,
                    batch_first = True,   # X shape = (batch_size, sequence_length, feature_count)
                    bidirectional = use_bidirectional
                )
            )

            # Update
            cur_layer_size = hidden_layer_size * self.direction_count

        return answers

    def forward(self, X: torch.Tensor) -> torch.Tensor:
        # X shape = (batch_size, sequence_length, input_layer_size)

        for rnn_layer in self.hidden_layers:
            X, _ = rnn_layer(X)                         # -> (batch_size, ...)

        last_time_step = X[:, -1, :]                    # -> (batch_size, last_hidden_size)
        predictions = self.output_layer(last_time_step) # -> (batch_size, output_layer_size)
        return predictions
