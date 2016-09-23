import csv
from Event import Event
from Runner import Runner
import numpy as np, re

def parseFile():
	marathon_dict = {}
	runner_list = []
	with open('Project1_data.csv', 'r', encoding='UTF-8') as f:
		reader = csv.reader(f, delimiter=',')
		next(reader) # skip header row
		for aLine in reader:
			number_of_marathons = (len(aLine) - 1) // 5
			runner_id = aLine[0]
			event_list = []
			for i in range(number_of_marathons):
				# Hacky way to access the information in a given line in the csv
				marathon_date = aLine[5*i + 1]
				marathon_name = aLine[5*i + 2]
				marathon_etype = aLine[5*i + 3]
				marathon_time = aLine[5*i + 4]
				marathon_category = aLine[5*i + 5]

				event_list.append(Event(marathon_date, # Create new Event and append to list
										marathon_name,
										marathon_etype,
										marathon_time,
										marathon_category))

				# Increments/initializes the values in the marathon_dict
				if marathon_name in marathon_dict:
					marathon_dict[marathon_name] = marathon_dict[marathon_name] + 1
				else:
					marathon_dict[marathon_name] = 1
			gender, age = parseCategory(aLine[5])
			runner_list.append(Runner(runner_id, event_list, gender, age)) # Create a new runner object and append to list

		""" Some code to help you get a better idea of the dataset, use this when you
			need some information about the number of marathons that exist

		for key in marathon_dict:
			if marathon_dict[key] < 500 and marathon_dict[key] > 300:
				print key, ": ", marathon_dict[key]
		"""
	return runner_list, marathon_dict

# parses a line of the csv file and creates
def parseCategory(category_field):
	# sets the gender 0 = male, 1 = female
	gender = 0
	if 'F' in category_field:
		gender = 1

	age = 30
	if '-' in category_field:
		try:
			category_field = re.match('[M|F][0-9][0-9]-[0-9][0-9]', category_field).group(0)
		except:
			pass
		age_ranges = category_field[1:].split('-')
		age_ranges = [int(s) for s in age_ranges if s.isdigit()]
		if len(age_ranges) > 1:
				age = sum(age_ranges)/len(age_ranges)
	return gender, age

def create_feature_matrix(runner_list):
	feat_width = 12 # magic number 12 for handcrafted features, always up for modification
	dim = (len(runner_list), feat_width)
	feat = np.zeros(dim)
	for idx in range(len(runner_list)):
		feat[idx,:] = runner_list[idx].get_feature()
	return feat

def create_participation_label(runner_list):
	dim = (len(runner_list), 1)
	labels = np.zeros(dim)
	for idx in range(len(runner_list)):
		labels[idx] =runner_list[idx].get_participation_label()
	return labels

def create_time_label(runner_list):
	dim = (len(runner_list), 1)
	labels = np.zeros(dim)
	for idx in range(len(runner_list)):
		labels[idx] =runner_list[idx].get_time_label()
	return labels

def get_error_classification(predictions, truths):
	idx = 0
	true_p, true_n, false_p, false_n = 0
	for idx in range(len(predictions)):
		if predictions[idx] == truths[idx] and predictions[idx] == 1:
			true_p = true_p + 1
		elif predictions[idx] == truths[idx] and predictions[idx] == 0:
			true_n = true_n + 1
		elif predictions[idx] != truths[idx] and predictions[idx] == 1:
			false_p = false_p + 1
		else:
			false_n = false_n + 1
	return true_p, true_n, false_p, false_n

def get_error_regression(prediction, truths):
	# TODO: implement least squares error between the times

	pass

def k_fold_cross_validation(X, Y, validation_fold_number, k):
	n = np.shape(X)[0]
	fold_size = n/k
	# indices = [14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
	indices = np.random.permutation(n) # shuffle, in case data is not i.i.d
	X = np.array(X)
	folds = [ X[indices[:fold_size]],X[indices[fold_size: fold_size*2]], X[indices[fold_size*2: fold_size*3]], X[indices[fold_size*3: fold_size*4]],X[indices[fold_size*4:]] ]
	Y_folds = [ Y[indices[:fold_size]],Y[indices[fold_size: fold_size*2]], Y[indices[fold_size*2: fold_size*3]], Y[indices[fold_size*3: fold_size*4]],Y[indices[fold_size*4:]] ]
	validation_fold, validation_Y, training_folds, training_Y = [], [], [], []
	for v in range(len(folds)):
		if v == validation_fold_number:
			validation_fold = np.array(folds[v])
			validation_Y = np.array(Y_folds[v])
		else:
			training_folds.append(folds[v])
			training_Y.append(Y_folds[v])
	training_folds = np.array(training_folds)
	training_Y = np.array(training_Y)
	return training_folds, training_Y, validation_fold, validation_Y

def main():
	runner_list, marathon_dict = parseFile()
	# print(len(runner_list))
	active_runner_list = [ r for r in runner_list if r.get_event("Oasis", "2015") != None and r.get_event("Oasis", "2015").get_time_in_seconds() != 0]
	# print len(runner_list)

	X = create_feature_matrix(active_runner_list)
	p_labels = create_participation_label(runner_list)
	t_labels = create_time_label(active_runner_list)

	# TODO: Calculate the errors for each model shown below in commented pseudocode

	# for a given model (i.g. logistic_regression, linear_regression, naiive_bayes):
	# for classification:
	k = 5
	prediction_error = []
	Y = p_labels
	for i in range(k):
		t_features, t_truths, v_features, v_truths = k_fold_cross_validation(X, Y, i, k)
		# print v_truths
		# model = fit_model(t_features, t_truths) # fit model with training data
		# predictions = predict(v_features) # retrieve predictions on validation data
		# error = get_error_classification(predictions, v_truths) # compare predictions with truths
		# prediction_error.append(error)
	total_prediction_error = np.mean(prediction_error)

	# for regression:
	k = 5
	prediction_error = []
	Y = t_labels
	for i in range(k):
		t_features, t_truths, v_features, v_truths = k_fold_cross_validation(X, Y, i, k)
		# print v_truths
		# model = fit_model(t_features, t_truths) # fit model with training data
		# predictions = predict(v_features) # retrieve predictions on validation data
		# error = get_error_regression(predictions, v_truths) # compare predictions with truths
		# prediction_error.append(error)
	total_prediction_error = np.mean(prediction_error)

if __name__ == '__main__':
	main()
