"""
@author Prev (prevdev@gmail.com)
"""
import sys
import math


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
			t = line.split('\t')
			ret.append((int(t[0]), int(t[1]), int(t[2]), t[3]))
		return ret

	def __init__(self, training_set, test_set):
		""" Init Recommender class instance
		:param training_set: List of tuple(user_id, item_id, rating, time_stamp)
		:param test_set: List of tuple(user_id, item_id, rating, time_stamp)
		"""
		training_set = training_set
		self.test_set = test_set

		self.user_set = {}
		self.item_dict = set()

		for user_id, item_id, rating, timestamp in training_set:
			if item_id not in self.item_dict:
				self.item_dict.add(item_id)
			if user_id not in self.user_set:
				self.user_set[user_id] = {}

			self.user_set[user_id][item_id] = int(rating)

	def predicate(self):
		""" Predicate relation (user_id -> item_id) with rating.
		:return: List of tuple(user_id, item_id, rating)
		"""
		item_dict = sorted(list(self.item_dict))

		for user_id, user in self.user_set.items():
			neighbors = self._neighbors(user)

			for item_id in item_dict:
				if item_id not in user:
					# Predicate item which is not existing in training set
					v = [u[item_id] for u in neighbors if item_id in u]
					if len(v) == 0:
						continue
					avg = sum(v) / len(v)

					# print("%d\t%d\t%d" % (user_id, item_id, avg))
					yield (user_id, item_id, round(avg))

	def _neighbors(self, user):
		""" Get neighbors of user.
		Criteria is set by heuristic, which cosine similarity is more than 0.97
		:param user: Dictionary value that has { item_id: rating } set
		:return: List of users
		"""
		ret = []
		for user_id, candidate in self.user_set.items():
			if user == candidate:
				continue
			if self._sim(user, candidate) >= 0.97:
				ret.append(candidate)
		return ret

	def _sim(self, user1, user2):
		""" Get similarity between user1 and user2
		:param user1: Dictionary value that has { item_id: rating } set
		:param user2: Dictionary value that has { item_id: rating } set
		:return: Similarity calculated by cosine similarity (0~1)
		"""
		# list of (rating1, rating2)
		v = [(rating1, user2[item_id]) for item_id, rating1 in user1.items() if item_id in user2]

		if len(v) == 0:
			return 0
		else:
			# Cosine Similarity
			return (
					sum([w1 * w2 for w1, w2 in v])
					/ math.sqrt(sum([w1 ** 2 for w1, w2 in v]))
					/ math.sqrt(sum([w2 ** 2 for w1, w2 in v]))
			)


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
	old_user_id = -1

	with open(output_filename, 'w') as output_file:
		for user_id, item_id, rating in rc.predicate():
			if old_user_id != user_id:
				print("now predicating user %s" % user_id)
				old_user_id = user_id

			output_file.write('%d\t%d\t%s\n' % (user_id, item_id, rating))

	print('Result is written at %s' % output_filename)
