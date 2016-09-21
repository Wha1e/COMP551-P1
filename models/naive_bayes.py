from sklearn import datasets
import numpy as np
import math

def gaussian_probs(x_vector, means, std_devs):
  exp_term = -(x_vector - means)**2 / (2 * std_devs**2)
  return 1/((2 * math.pi)**(1/2) * std_devs) * np.exp(exp_term)

def bernoulli_probs():
  return 1

def predict(X, **kwargs):
  predictions = []

  for x_values in X:
    means = kwargs["means"]
    std_devs = kwargs["std_devs"]
    priors = kwargs["priors"]

    if (means.shape != std_devs.shape):
      print("mean matrix and standard dev matrix don't have the same shape")
      return

    num_classes = len(means)

    def likelihood(gaussian_probs):
      return np.prod(gaussian_probs)

    class_probabilities = np.array([
      likelihood(gaussian_probs(x_values, means[c], std_devs[c])) * 
      likelihood(bernoulli_probs()) *
      priors[c]
      for c in range(num_classes)
    ])
    
    predictions.append(class_probabilities.argmax())

  return np.array(predictions)

def get_data_params(X, Y):
  if (len(X) != len(Y)):
    print("The number of entries is not equal to the number of results")
    return

  num_entries = len(X)
  means = []
  std_devs = []
  priors = []
  classes = np.unique(Y)
  combined_data = np.column_stack((X, Y))

  for c in classes:
    class_data = np.array([entry for entry in combined_data if entry[-1] == c])
    x_values = class_data[:, :-1]
    means.append(np.mean(x_values, axis=0))
    std_devs.append(np.std(x_values, axis=0))
    priors.append(len(class_data)/num_entries)

  return {
    "classes": classes,
    "means": np.array(means),
    "std_devs": np.array(std_devs),
    "priors": np.array(priors)
  }

if __name__ == "__main__":
  data = datasets.load_iris()
  X = data.data[:100, :2]
  Y = data.target[:100]

  data_params = get_data_params(X, Y)

  predictions = predict(X, **data_params)
  correct_predictions = np.sum(predictions == Y)

  print("Correct predictions: " + str(correct_predictions) + "/" + str(Y.size))

