import torch
from torch import nn
from torch.utils.data import TensorDataset
from torch.utils.data import DataLoader # for splitting X_train into mini-batches

def build_tensor(x, is_regression=True) -> torch.Tensor:
    """float tensor for regression; long tensor for classification"""
    dtype = torch.float32 if is_regression else torch.long
    return torch.as_tensor(x, dtype=dtype)

def fit(
    X_and_y: TensorDataset, model: nn.Module, 
    loss_func: nn.Module, optimizing_func,
    lr = 1e-3, max_epoch = 5, batch_size = None
): # -> model

    # Step 1: mini-batch
    if not batch_size: batch_size = len(X_and_y)
    batches = DataLoader(X_and_y, batch_size=batch_size, shuffle=True)
    
    # Step 2: turn on 'train' mode (the other is 'eval' / prediction mode)
    model.train(True)

    # Step 3
    optimizer = optimizing_func(model.parameters(), lr = lr)
    for _ in range(max_epoch): # 1 epoch = entire 'batches' train
        for batch in batches:

            # Reset all gradients to 0
            optimizer.zero_grad()

            # batch = (X, y) or (input_ids, attention_maxk, y)
            *X_train, y_train = batch

            # Forward-Propagation
            y_pred = model(*X_train) # auto call model.forward()
            loss = loss_func(y_pred, y_train)

            # Back-Propagation
            loss.backward()     # compute all gradients
            optimizer.step()    # update weights

    return model

def predict(
    X_test: TensorDataset,
    trained_model: nn.Module,
    batch_size = None
) -> torch.Tensor:

    if not batch_size: batch_size = len(X_test)
    batches = DataLoader(X_test, batch_size, shuffle=False)

    # Step 2: Turn on predict mode
    trained_model.eval()

    answers = []
    for X_batch in batches:

        # pred_y's dimension is (batch_size, ...)
        pred_y = trained_model(*X_batch)
        answers.append(pred_y.cpu()) # .cpu() for safe Numpy and not need to rely on GPU

    # Stack batches to 1 tensor (batch1 + batch2 + ..., ...)
    return torch.cat(answers)
