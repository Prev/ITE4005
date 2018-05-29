"""
@author Prev (prevdev@gmail.com)
"""
import sys

class Recommender:

	@staticmethod
	def file2dataset(input_file):
		""" Parse input file and convert it to list. File format is like below
		[user_id]\t[item_id]\t[rating]\t[time_stamp]\n
		[user_id]\t[item_id]\t[rating]\t[time_stamp]\n
		...
		:param input_file: Training or testing file opened
		:return:
		"""
		ret = []
		for line in input_file.readlines():
			if line[-1] == '\n': line = line[0:-1]
			ret.append(tuple(line.split('\t')))
		return ret


	def __init__(self, training_set, test_set):
		""" Init Recommender class instance
		:param training_set: List of tuple(user_id, item_id, rating, time_stamp)
		:param test_set: List of tuple(user_id, item_id, rating, time_stamp)
		"""
		self.training_set = training_set
		self.test_set = test_set


	def predicate(self):
		""" Predicate relation (user_id -> item_id) with rating.
		:return: List of tuple(user_id, item_id, rating)
		"""
		return []


if __name__ == '__main__':
	if len(sys.argv) != 3:
		print("Usage: python recommender.py <training_data> <test_data>")
		sys.exit(-1)

	training_file_name = sys.argv[1]
	test_file_name = sys.argv[1]

	rc = Recommender(
		Recommender.file2dataset(open(training_file_name, 'r')),
		Recommender.file2dataset(open(test_file_name, 'r')),
	)

	output_filename = training_file_name.split('.')[0] + '.base_prediction.txt'
	with open(output_filename, 'w') as output_file:
		for user_id, item_id, rating in rc.predicate():
			output_file.write('%d\t%d\t%s\n' % (user_id, item_id, rating))

	print('Result is written at %s' % output_filename)
