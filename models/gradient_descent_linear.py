import numpy as np

def grad_desc_linear(data, learning_rate, error_margin):
  training_params = data[:, :-1]
  training_results = data[:, [-1]]

  num_features = training_params.shape[1]
  weights = np.zeros((num_features, 1)) # initial weights of 0

  for i in range(100):
    first_term = training_params.T.dot(training_params).dot(weights)
    second_term = training_params.T.dot(training_results)

    derivative_term = 2.0 * (first_term - second_term)
    new_weights = weights - learning_rate * derivative_term

    largest_weight_diff = abs(new_weights - weights).max()
    if (largest_weight_diff <= abs(error_margin)): # is this correct?
      print("converged!")
      return new_weights
    else:
      weights = new_weights

  print("diverged...")
  return -1

if __name__ == "__main__":
  data = np.array([
    [0.86, 1, 2.49],
    [0.09, 1, 0.83],
    [-0.85, 1, -0.25],
    [0.87, 1, 3.10],
    [-0.44, 1, 0.87],
    [-0.43, 1, 0.02],
    [-1.1, 1, -0.12],
    [0.40, 1, 1.81],
    [-0.96, 1, -0.83],
    [0.17, 1, 0.43]
  ])

  weights = grad_desc_linear(data, 0.09, 0.05)
  print(weights)
