import torch
from torch import nn

class Transformers(nn.Module):
    def __init__(
        self,
        vocabulary_size: int,
        output_layer_size: int,     # regression: 1, classification: class_count

        model_dimension: int = 64,
        attention_head_count: int = 4,
        encoder_layer_count: int = 2,
        max_token_count: int = 256
    ):
        super().__init__()

        self.token_embedding = nn.Embedding(vocabulary_size, model_dimension)
        self.position_embedding = nn.Embedding(max_token_count, model_dimension)

        encoder_layer = nn.TransformerEncoderLayer(
            d_model = model_dimension,
            nhead = attention_head_count,
            batch_first = True
        )
        self.hidden_layers = nn.TransformerEncoder(
            encoder_layer,
            num_layers = encoder_layer_count
        )

        # Connect to output layer
        self.output_layer = nn.Linear(model_dimension, output_layer_size)

    def forward(self, input_ids: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
        # input_ids shape      = (batch_size, token_count)
        # attention_mask shape = (batch_size, token_count)

        batch_size, token_count = input_ids.shape

        position_ids = torch.arange(token_count, device=input_ids.device)
        position_ids = position_ids.unsqueeze(0).expand(batch_size, token_count)

        token_vectors = self.token_embedding(input_ids)
        position_vectors = self.position_embedding(position_ids)
        encoder_input = token_vectors + position_vectors

        padding_locations = (attention_mask == 0)
        token_hidden_states = self.hidden_layers(
            encoder_input, padding_locations
        )

        pooled_vector = self._mean_pool_over_tokens(token_hidden_states, attention_mask)

        # predictions shape = (batch_size, output_layer_size)
        predictions = self.output_layer(pooled_vector)
        return predictions
    
    def _mean_pool_over_tokens(self, token_hidden_states: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
        mask = attention_mask.unsqueeze(-1).float()           # (batch_size, token_count, 1)
        masked_sum = (token_hidden_states * mask).sum(dim=1)  # (batch_size, model_dimension)
        token_count = mask.sum(dim=1).clamp_min(1.0)          # (batch_size, 1)
        pooled_vector = masked_sum / token_count              # (batch_size, model_dimension)
        return pooled_vector
