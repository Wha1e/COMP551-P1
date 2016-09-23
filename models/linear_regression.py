import numpy as np

class LinearRegression():
  def __init__(self):
    self.predictions = None
    self.weights = None

  @staticmethod
  def normalize(X):
    std_dev = np.std(X, axis=0)
    return (X - np.mean(X, axis=0)) / np.std(X, axis=0)

  def fit(self, X, Y, learning_rate=0.00005, error_margin=0.005):
    X = np.column_stack((X, np.ones(len(X))))
    num_features = X.shape[1]
    weights = np.zeros((num_features, 1)) # initial weights of 0

    for i in range(10000):
      first_term = X.T.dot(X).dot(weights)
      second_term = X.T.dot(Y)

      derivative_term = 2.0 * (first_term - second_term)
      new_weights = weights - learning_rate * derivative_term

      largest_weight_diff = abs(new_weights - weights).max()
      if (largest_weight_diff <= abs(error_margin)):
        self.weights = new_weights
        return
      else:
        weights = new_weights

    print("diverged...")
    return -1

  def predict(self, X):
    X = np.column_stack((X, np.ones(len(X))))
    self.predictions = np.array([x.dot(self.weights).item() for x in X])
    return self.predictions

  def get_success_rate(self, Y):
    diff = np.absolute(self.predictions - Y)
    return np.mean(diff)

if __name__ == "__main__":
  lr = LinearRegression()

  X = LinearRegression.normalize(np.load("../data/active_runner_feat.npy"))
  Y = np.load("../data/active_runner_labels.npy")

  lr.fit(X, Y)
  predictions = lr.predict(X)

  sr = lr.get_success_rate(Y)
  print(sr)
