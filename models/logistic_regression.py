from sklearn import linear_model
import numpy as np
import math
import matplotlib.pyplot as plt

class LogisticRegression():
  def __init__(self):
    self.weights = None
    self.predictions = None
    self.errors = []

  def logistic_func(self, weights, training_params):
    exp_term = weights.dot(training_params)
    return 1/(1 + math.exp(-(exp_term)))

  def error_func(self, weights, X, Y):
    return -np.sum( [Y[i] * math.log(self.logistic_func(weights, x)) + (1 - Y[i]) * math.log(1 - self.logistic_func(weights, x)) for i,x in enumerate(X) ])

  @staticmethod
  def normalize(X):
    return (X - np.mean(X, axis=0)) / np.std(X, axis=0)

  def fit(self, X, Y, learning_rate=0.0005, error_margin=0.001):
    num_features = X.shape[1]
    weights = np.zeros(num_features) # initial weights of 0

    errors = []
    for idx in range(10000):
      vector_sum = np.zeros(num_features)

      for i, x in enumerate(X):
        y = Y[i]
        vector_sum += x * (self.logistic_func(weights, x) - y)

      new_weights = weights - learning_rate * vector_sum

      error = self.error_func(new_weights, X, Y)
      errors.append(error)

      largest_weight_diff = abs(new_weights - weights).max()
      if (largest_weight_diff <= abs(error_margin)):
        self.weights = new_weights
        # self.generate_graph(errors)
        return
      else:
        weights = new_weights

    # self.generate_graph(self.errors)
    print("diverged...")
    return -1

  def generate_graph(self, errors):
    plt.plot(errors, 'bo')
    plt.axis([0, 100, 3300, 3600])
    plt.xlabel('Iterations')
    plt.ylabel('Value of Cost Function')
    plt.title('Value of Cost Function vs Number of Iterations of Gradient Descent for Logistic Regression Model')
    plt.show()

  def get_error_classification(self, predictions, truths):
      idx = 0
      true_p, true_n, false_p, false_n = 0, 0, 0, 0
      for idx in range(len(predictions)):
          if predictions[idx] == truths[idx] and predictions[idx] == 1:
              true_p = true_p + 1
          elif predictions[idx] == truths[idx] and predictions[idx] == 0:
              true_n = true_n + 1
          elif predictions[idx] != truths[idx] and predictions[idx] == 1:
              false_p = false_p + 1
          else:
              false_n = false_n + 1
      return true_p, true_n, false_p, false_n

  def predict(self, X):
    self.predictions = np.array([1 if self.logistic_func(self.weights, x) >= 0.5 else 0 for x in X])
    return self.predictions

  def get_success_rate(self, Y):
    return np.sum(self.predictions == Y[:, 0])/len(Y)
