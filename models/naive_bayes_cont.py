from sklearn import datasets
import numpy as np
import math

class NaiveBayes():
  def __init__(self):
    self.data_params = None
    self.predictions = None

  @staticmethod
  def gaussian_probs(x_vector, means, std_devs):
    exp_term = -(x_vector - means)**2 / (2 * std_devs**2)
    return 1/((2 * math.pi)**(1/2) * std_devs) * np.exp(exp_term)

  def fit(self, X, Y):
    if (len(X) != len(Y)):
      print("The number of entries is not equal to the number of results")
      return

    num_total_entries = len(X)
    means = []
    std_devs = []
    priors = []
    classes = np.unique(Y)

    for c in classes:
      x = [np.array(x) for x, y in zip(X, Y) if y == c]
      num_class_entries = len(x)

      means.append(np.mean(x, axis=0))
      std_devs.append(np.std(x, axis=0))
      priors.append(num_class_entries/num_total_entries)

    self.data_params = {
      "classes": classes,
      "means": np.array(means),
      "std_devs": np.array(std_devs),
      "priors": np.array(priors)
    }

  def predict(self, X):
    predictions = []

    means = self.data_params["means"]
    std_devs = self.data_params["std_devs"]
    priors = self.data_params["priors"]

    num_classes = len(means)

    def likelihood(probs):
      return np.prod(probs)

    for x_vector in X:
      class_probabilities = np.array([
        likelihood(NaiveBayes.gaussian_probs(x_vector, means[c], std_devs[c])) * 
        priors[c]
        for c in range(num_classes)
      ])
      
      predictions.append(class_probabilities.argmax())

    self.predictions = np.array(predictions)
    return self.predictions

  def get_success_rate(self, Y):
    return np.sum(self.predictions == Y[:, 0])/len(Y)

if __name__ == "__main__":
  data = datasets.load_iris()
  X = data.data[:100, :2]
  Y = data.target[:100]
  Y = Y.reshape(len(Y), 1)

  nb = NaiveBayes()
  nb.fit(X, Y)
  predictions = nb.predict(X)
  print("Correct predictions: " + str(nb.get_success_rate(Y)))

