import numpy as np

class LinearRegression():
  def __init__(self):
    self.predictions = None
    self.weights = None

  @staticmethod
  def normalize(X):
    return (X - np.mean(X, axis=0)) / np.std(X, axis=0)

  def fit(self, X, Y):
    self.weights = np.linalg.inv(X.T.dot(X)).dot(X.T.dot(Y)) # closed form
    return self.weights

  def predict(self, X):
    self.predictions = np.array([x.dot(self.weights).item() for x in X])
    return self.predictions

  def get_success_rate(self, Y):
    diff = np.absolute(self.predictions - Y)
    return np.mean(diff)
