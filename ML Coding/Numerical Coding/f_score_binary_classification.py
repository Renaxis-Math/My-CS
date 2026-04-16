"""
Implement F-Score Calculation for Binary Classification
Task: Implement F-Score Calculation for Binary Classification
Your task is to implement a function that calculates the F-Score for a binary classification task. The F-Score combines both Precision and Recall into a single metric, providing a balanced measure of a model's performance.

Write a function f_score(y_true, y_pred, beta) where:

y_true: A numpy array of true labels (binary).
y_pred: A numpy array of predicted labels (binary).
beta: A float value that adjusts the importance of Precision and Recall. When beta=1, it computes the F1-Score, a balanced measure of both Precision and Recall.
The function should return the F-Score rounded to three decimal places.

Example
Example:
import numpy as np

y_true = np.array([1, 0, 1, 1, 0, 1])
y_pred = np.array([1, 0, 1, 0, 0, 1])
beta = 1

print(f_score(y_true, y_pred, beta))

# Expected Output:
# 0.857
"""

import numpy as np

def f_score(y_true, y_pred, beta):
    tp = np.sum((y_true == 1) & (y_pred == 1))
    fn = np.sum((y_true == 1) & (y_pred == 0))
    fp = np.sum((y_true == 0) & (y_pred == 1))

    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0

    op = precision * recall
    div = ((beta**2) * precision) + recall

    if div == 0 or op == 0:
        return 0.0

    score = (1 + (beta ** 2)) * op / div
    return round(score, 3)
