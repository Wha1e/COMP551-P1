import Parser
import numpy as np, csv
from models.logistic_regression import LogisticRegression
from models.linear_regression import LinearRegression
from models.naive_bayes_cont import NaiveBayes
import models.cross_validation as cv


def get_classification_training_data():
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

def get_classification_testing_data():
    # Includes 2015 Montreal Oasis data
    all_runners, _ = Parser.parseFile()

    X = np.array([
      [
        r.get_total_full_races(),
        len([e for e in r.events if "Oasis" in e.name and e.etype == "Marathon"]),
        len([e for e in r.events if "2016" in e.date]),
      ]
      for r in all_runners
    ])
    return X

def get_regression_testing_data():
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
  X, Y = get_classification_training_data()
  test_X = get_classification_testing_data()

  models = [LogisticRegression(), NaiveBayes()]
  predictions = []
  for model in models:
      model.fit(X, Y)
      predictions.append(model.predict(test_X))

  runner_ids = np.arange(len(Y))
  all_predictions = zip(runner_ids, predictions[0], predictions[1])

  with open("data/predictions.csv", "w") as outfile:
      csv_out = csv.writer(outfile)
      for row in all_predictions:
          csv_out.writerow(row)
