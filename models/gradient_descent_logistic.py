from sklearn import datasets
import numpy as np
import math

def logistic_func(weights, training_params):
  return 1/(1 + math.exp(-(weights.dot(training_params))))

def normalize(X):
  return (X - np.mean(X, axis=0)) / np.std(X, axis=0)

def grad_desc_logistic(X, Y, learning_rate, error_margin):
  num_features = X.shape[1]
  X = normalize(X)
  weights = np.zeros(num_features) # initial weights of 0

  for i in range(500):
    vector_sum = np.zeros(num_features)

    for i, x in enumerate(X):
      y = Y[i]
      vector_sum += x * (logistic_func(weights, x) - y)

    new_weights = weights - learning_rate * vector_sum

    largest_weight_diff = abs(new_weights - weights).max()
    if (largest_weight_diff <= abs(error_margin)): # is this correct?
      print("converged in {} iterations".format(i + 1))
      return new_weights
    else:
      weights = new_weights

  print("diverged...")
  return -1      

def predict(weights, X):
  X = normalize(X)
  predictions = [1 if logistic_func(weights, x) >= 0.5 else 0 for x in X]
  return predictions

if __name__ == "__main__":
  data = datasets.load_iris()
  X = data.data[:100, :2]
  Y = data.target[:100]
  Y = np.logical_not(Y)

  predicted_weights = grad_desc_logistic(X, Y, 0.001, 0.003)
  predictions = predict(predicted_weights, X)
  correct_predictions = np.sum(predictions == Y)

  print("Correct predictions: " + str(correct_predictions) + "/" + str(Y.size))
