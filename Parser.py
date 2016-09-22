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

def evaluate_prediction(predictions, truths):
	idx = 0
	hits = 0
	misses = 0
	for idx in range(len(predictions)):
		if predictions[idx] == truths[idx]:
			hits = hits + 1
		else:
			misses = misses + 1
	return hits, misses

def k_fold_cross_validation(X, Y, validation_fold_number):
	k = 5
	n = np.shape(X)[0]
	fold_size = n/k
	indices = np.random.permutation(n) # shuffle, in case data is not i.i.d
	X = np.array(X)
	folds = [ X[indices[:fold_size]],X[indices[fold_size: fold_size*2]], X[indices[fold_size*2: fold_size*3]], X[indices[fold_size*3: fold_size*4]],X[indices[fold_size*4:]] ]
	Y_folds = [ Y[indices[:fold_size]],Y[indices[fold_size: fold_size*2]], Y[indices[fold_size*2: fold_size*3]], Y[indices[fold_size*3: fold_size*4]],Y[indices[fold_size*4:]] ]
	# validation_fold_number = 0
	validation_fold = []
	validation_Y = []
	training_folds = []
	training_Y = []
	for v in range(len(folds)):
		if v == validation_fold_number:
			validation_fold = np.array(folds[v])
			validation_Y = np.array(Y_folds[v])
		else:
			training_folds.append(folds[v])
			training_Y = np.array(Y_folds[v])
	training_folds = np.array(training_folds)
	# print len(training_folds)
	return training_folds.flatten(), training_Y.flatten(), validation_fold, validation_Y

def main():
	# runner_list, marathon_dict = parseFile()
	# print(len(runner_list))
	# active_runner_list = [ r for r in runner_list if r.get_event("Oasis", "2015") != None and r.get_event("Oasis", "2015").get_time_in_seconds() != 0]
	# print len(runner_list)

	# for r in runner_list:
	# 	print r.get_event("Oasis", "2015").get_time_in_seconds()

	# feat = create_feature_matrix(active_runner_list)
	# p_labels = create_participation_label(runner_list)
	# t_labels = create_time_label(active_runner_list)
	# np.save("data/active_runner_feat", feat)
	# np.save("data/active_runner_labels", t_labels)
	# print feat
	# print np.shape(feat) # sanity check => should have (8711, 12) as our feature matrix dimension

	X = np.random.rand(15,5)
	X = [10*x for x in X]
	# X = np.array([0,1,2,3,4],[0,2,2,2,2],[1,2,3,1,2])
	Y = np.array([0,1,1,0,1,0,1,1,1,0,0,0,0,1,1,0])
	t_folds, t_Y, v_fold, v_Y = k_fold_cross_validation(X,Y, 0)
	print np.shape(t_folds), np.shape(t_Y), np.shape(v_fold), np.shape(v_Y)

if __name__ == '__main__':
	main()
