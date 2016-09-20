import csv
from Event import Event
from Runner import Runner

def parseFile():
	marathon_dict = {}
	runner_list = []
	with open('Project1_data.csv', 'r') as f:
		reader = csv.reader(f, delimiter=',')
		for aLine in reader:
			number_of_marathons = (len(aLine) - 1) / 5
			runner_id = aLine[0]
			event_list = []
			for i in range(number_of_marathons):

				# Hacky way to access the information in a given line in the csv
				marathon_date = aLine[((number_of_marathons - 1 )*5) + 1]
				marathon_name = aLine[((number_of_marathons - 1 )*5) + 2]
				marathon_etype = aLine[((number_of_marathons - 1 )*5) + 3]
				marathon_time = aLine[((number_of_marathons - 1 )*5) + 4]
				marathon_category = aLine[((number_of_marathons - 1 )*5) + 5]

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
		age_ranges = category_field[1:].split('-')
		if len(age_ranges[1]) == 1:
			age_ranges = [int(i.strip()) for i in age_ranges]
			age = sum(age_ranges)/len(age_ranges)

	return gender, age


def main():
	runner_list, marathon_dict = parseFile()
	print runner_list[3].events

if __name__ == '__main__':
	main()