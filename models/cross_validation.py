import numpy as np

def cross_validate(X, Y, model_class, k=5):
  combined_data = np.column_stack((X, Y))
  np.random.shuffle(combined_data)
  split_data = np.array_split(combined_data, k)
  success_rates = []

  for i in range(k):
    training_data = np.concatenate([split_data[j] for j in range(k) if j != i])
    validation_data = np.array(split_data[i])

    X_training = training_data[:, :-1]
    Y_training = training_data[:, [-1]]

    model = model_class()
    model.fit(X_training, Y_training)

    X_validation = validation_data[:, :-1]
    Y_validation = validation_data[:, [-1]]

    predictions = model.predict(X_validation)
    # true_p, true_n, false_p, false_n = model.get_error_classification(predictions, Y_validation)
    success_rate = model.get_success_rate(Y_validation)
    success_rates.append(success_rate)
    print("Fold #{}: {}".format(i + 1, success_rate))

  print("Average success rate: {}".format(np.mean(success_rates)))
