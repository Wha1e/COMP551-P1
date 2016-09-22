from sklearn import linear_model
import numpy as np

def normalize(X):
  std_dev = np.std(X, axis=0)
  return (X - np.mean(X, axis=0)) / np.std(X, axis=0)

def grad_desc_linear(X, Y, learning_rate, error_margin):
  num_features = X.shape[1]
  weights = np.zeros((num_features, 1)) # initial weights of 0

  for i in range(10000):
    first_term = X.T.dot(X).dot(weights)
    second_term = X.T.dot(Y)

    derivative_term = 2.0 * (first_term - second_term)
    new_weights = weights - learning_rate * derivative_term

    largest_weight_diff = abs(new_weights - weights).max()
    if (largest_weight_diff <= abs(error_margin)): # is this correct?
      print("converged in " + str(i) + " iterations!")
      return new_weights
    else:
      weights = new_weights

  print("diverged...")
  return -1

def predict(weights, X):
  return np.array([x.dot(weights).item() for x in X])

def sklearn_prediction(X, Y):
  lr = linear_model.LinearRegression()
  lr.fit(X, np.ravel(Y))
  predictions = lr.predict(X[:100])
  diff = np.absolute(predictions - Y[:100])
  mean = np.mean(diff)
  print(mean)


if __name__ == "__main__":
  X = normalize(np.load("../data/active_runner_feat.npy"))[:, [2]]
  X = np.column_stack((X, np.ones(len(X))))
  Y = np.load("../data/active_runner_labels.npy")

  predictions = predict(grad_desc_linear(X, Y, 0.00005, 0.005), X[:100])
  diff = np.absolute(predictions - Y[:100])
  mean = np.mean(diff)
  print(mean)
