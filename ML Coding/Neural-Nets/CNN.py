import torch
from torch import nn

class CNN(nn.Module):
    def __init__(self,
        # image = H * W * D, D = how many values per pixel. E.g: colored image -> (R, G, B) -> 3
        image_depth: int,
        hidden_layer_sizes: list[int],
        maxPool_window_size = 1,    # NEW. 1 = not use MaxPooling
        activation_func = nn.ReLU
    ):
        super().__init__()

        self.network = nn.Sequential(
            *self._build_hidden_layers(
                image_depth,
                hidden_layer_sizes,
                maxPool_window_size,
                activation_func
            )
        )

    def _build_hidden_layers(
        self, 
        image_depth, 
        hidden_layer_sizes,
        maxPool_window_size,
        activation_func
    ) -> list[nn.Module]:
        
        answers = []

        cur_layer_size = image_depth
        for hidden_layer_size in hidden_layer_sizes:
            answers.append(nn.Conv2d(cur_layer_size, hidden_layer_size, kernel_size=3, padding=1))
            answers.append(activation_func())
            
            # if use MaxPool aka window_size > 1, we want strongest signal pixel 
            if maxPool_window_size > 1:
                answers.append(nn.MaxPool2d(maxPool_window_size))

            # Update
            cur_layer_size = hidden_layer_size

        return answers

    def forward(self, image_tensor: torch.Tensor) -> torch.Tensor:
        # image_tensor shape = (batch_size, image_depth, height, width)
        # features shape = (batch_size, last_hidden_layer_size, new_height, new_width)      
        features = self.network(image_tensor)
        return features