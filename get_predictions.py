import Parser
import numpy as np, csv
from models.logistic_regression import LogisticRegression
from models.linear_regression import LinearRegression
from models.naive_bayes_cont import NaiveBayes
import models.cross_validation as cv
import datetime

def save_to_csv(data, filename):
  with open(filename, "w") as outfile:
      csv_out = csv.writer(outfile)
      for row in data:
          csv_out.writerow(row)

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
  Y = np.array([[r.get_participation_label()] for r in all_runners])

  feature_file = "data/classification_training_features.csv"
  labels_file = "data/classification_training_labels.csv"
  print("saving classification training features and labels in", feature_file, "and", labels_file)
  save_to_csv(X, feature_file)
  save_to_csv(Y, labels_file)

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

    feature_file = "data/classification_testing_features.csv"
    print("saving classification test features in", feature_file)
    save_to_csv(X, feature_file)

    return X

def get_regression_training_data():
  all_runners, _ = Parser.parseFile()

  runners_with_finishing_time = [r for r in all_runners if r.get_time_label() != -1 and r.get_avg_full_marathon_without_label() != -1]

  X = np.array([
    [
      r.get_total_full_races() - r.get_participation_label(),
      r.age,
      r.get_avg_full_marathon_without_label()
    ]
    for r in runners_with_finishing_time
  ])
  Y = np.array([[r.get_time_label()] for r in runners_with_finishing_time])

  feature_file = "data/regression_training_features.csv"
  labels_file = "data/regression_training_labels.csv"
  print("saving regression training features and labels in", feature_file, "and", labels_file)
  save_to_csv(X, feature_file)
  save_to_csv(Y, labels_file)

  return X, Y

def get_regression_testing_data():
  all_runners, _ = Parser.parseFile()

  X = np.array([
    [
      r.get_total_full_races(),
      r.age,
      r.get_avg_full_marathon_time()
    ]
    for r in all_runners
  ])

  feature_file = "data/regression_testing_features.csv"
  print("saving regression test features in", feature_file)
  save_to_csv(X, feature_file)

  return X

def generate_classification_predictions():
  X, Y = get_classification_training_data()
  test_X = get_classification_testing_data()

  class_models = [LogisticRegression(), NaiveBayes()]
  predictions = []
  for model in class_models:
    model.fit(X, Y)
    predictions.append(model.predict(test_X))
  
  return predictions

def generate_regression_predictions():
  X, Y = get_regression_training_data()
  test_X = get_regression_testing_data()

  lr = LinearRegression()
  lr.fit(X, Y)
  predictions = [str(datetime.timedelta(seconds=int(s))) for s in lr.predict(test_X)]

  for i, x in enumerate(test_X):
    # set those who don't have a full marathon to -1
    if x[2] == -1:
      predictions[i] = -1

  return predictions

def generate_predictions():
  print("generating predictions...")

  class_predictions = generate_classification_predictions()
  lin_reg_predictions = generate_regression_predictions()

  runner_ids = np.arange(len(lin_reg_predictions))
  all_predictions = zip(runner_ids, class_predictions[0], class_predictions[1], lin_reg_predictions)

  save_to_csv(all_predictions, "predictions/predictions.csv")

  print("predictions generated in predictions/predictions.csv")

if __name__ == "__main__":
  generate_predictions()
