from typing import List, Any
import random

class Bootstrap:
    def __init__(self, n_estimators: int = 100):
        self.n_estimators = n_estimators
        self.classifiers = None

    def bootsample(self, n: int) -> List[int]:
        return [random.randint(0, n-1) for _ in range(n)]

    def fit(self, classifiers: List[Any], x: List[List[float]], y: List[float]) -> None:
        self.classifiers = classifiers
        
        for clf in self.classifiers:
            indices = self.bootsample(len(x))
            x_boot = [x[i] for i in indices]
            y_boot = [y[i] for i in indices]
            clf.fit(x_boot, y_boot)

    def predict(self, x_test: List[float]) -> float:
        predictions = [clf.predict([x_test])[0] for clf in self.classifiers]
        
        # Majority voting
        return max(set(predictions), key=predictions.count)

# Example usage:
# from sklearn.tree import DecisionTreeClassifier
# 
# # Create a list of base classifiers
# base_classifiers = [DecisionTreeClassifier() for _ in range(100)]
# 
# # Create and use the Bootstrap ensemble
# bootstrap = Bootstrap(n_estimators=100)
# 
# # x is a list of lists, where each inner list is a list of floats
# x = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6], [0.7, 0.8, 0.9]]
# y = [0.0, 1.0, 0.0]  # y is a list of floats
# 
# bootstrap.fit(base_classifiers, x, y)
# 
# # x_test is a list of floats representing a single sample
# x_test = [0.2, 0.3, 0.4]
# prediction = bootstrap.predict(x_test)
# print(f"Prediction for {x_test}: {prediction}")