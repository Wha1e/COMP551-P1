from sklearn import linear_model
import numpy as np
import math

class LogisticRegression():
  def __init__(self):
    self.weights = None

  def logistic_func(self, weights, training_params):
    exp_term = weights.dot(training_params)
    return 1/(1 + math.exp(-(exp_term)))

  @staticmethod
  def normalize(X):
    std_dev = np.std(X, axis=0)
    return (X - np.mean(X, axis=0)) / np.std(X, axis=0)

  def fit(self, X, Y, learning_rate=0.001, error_margin=0.5):
    num_features = X.shape[1]
    weights = np.zeros(num_features) # initial weights of 0

    for i in range(10000):
      vector_sum = np.zeros(num_features)

      for i, x in enumerate(X):
        y = Y[i]
        vector_sum += x * (self.logistic_func(weights, x) - y)

      new_weights = weights - learning_rate * vector_sum

      largest_weight_diff = abs(new_weights - weights).max()
      if (largest_weight_diff <= abs(error_margin)): # is this correct?
        print("converged in {} iterations".format(i + 1))
        self.weights = new_weights
        return
      else:
        weights = new_weights

    print("diverged...")
    return -1      

  def predict(self, X):
    predictions = np.array([1 if self.logistic_func(self.weights, x) >= 0.5 else 0 for x in X])
    return predictions
