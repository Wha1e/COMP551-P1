import Parser
import numpy as np
from models.logistic_regression import LogisticRegression
from models.linear_regression import LinearRegression
from models.naive_bayes_cont import NaiveBayes
import models.cross_validation as cv

def get_participation_data():
  all_runners, _ = Parser.parseFile()

  X = np.array([
    [
      r.get_total_full_races() - r.get_participation_label(),
      len([e for e in r.events if "Oasis" in e.name and e.etype == "Marathon"]) - r.get_participation_label(),
      len([e for e in r.events if "2015" in e.date]) - r.get_participation_label(),
    ]
    for r in all_runners
  ])
  Y = np.array([r.get_participation_label() for r in all_runners])
  return X, Y

def get_finishing_time_data():
  all_runners, _ = Parser.parseFile()

  runners_with_finishing_time = [r for r in all_runners if r.get_time_label() != -1]

  X = np.array([
    [
      r.get_avg_oasis_time()
    ]
    for r in runners_with_finishing_time
  ])
  Y = np.array([r.get_time_label() for r in runners_with_finishing_time])

  return X, Y


if __name__ == "__main__":
  X, Y = get_participation_data()
  X = LogisticRegression.normalize(X)
  cv.cross_validate(X, Y, LogisticRegression)
  # cv.cross_validate(X, Y, NaiveBayes)

  # X = LogisticRegression.normalize(np.load("data/feat.npy"))
  # Y = np.load("data/labels.npy")
  # cv.cross_validate(X, Y, NaiveBayes)

  # X, Y = get_finishing_time_data()
  # print(X)
  # print(Y)

  # all_runners, _ = Parser.parseFile()
  # for r in all_runners:
    # r.get_all_events()


  # X_lin = LinearRegression.normalize(np.load("../data/active_runner_feat.npy"))
  # Y_lin = np.load("../data/active_runner_labels.npy")
  # cross_validate(X_lin, Y_lin, LinearRegression)
