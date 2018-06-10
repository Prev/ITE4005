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
		""" Init Recommender class instance and prepare for predicating
		:param training_set: List of tuple(user_id, item_id, rating, time_stamp)
		:param test_set: List of tuple(user_id, item_id, rating, time_stamp)
		"""
		self.test_set = test_set
		data = {}

		# You can get rating by accessing `data[user_id][item_id]`
		for user_id, item_id, rating, timestamp in training_set:
			if user_id not in data:
				data[user_id] = {}
			data[user_id][item_id] = rating

		# Pre-build-up neighbors
		self.neighbors_dict = {}
		for user_id, user in data.items():
			self.neighbors_dict[user_id] = self._neighbors(
				user=user,
				allusers=data.values()
			)


	def predicate(self):
		""" Predicate relation (user_id -> item_id) with rating.
		:return: List of tuple(user_id, item_id, rating)
		"""
		for user_id, item_id, real_rating, _ in self.test_set:
			# Predicate rating by calculating average of neighbors
			v = [u[item_id] for u in self.neighbors_dict[user_id] if item_id in u]
			if len(v) == 0:
				rating = 2
			else:
				rating = round(sum(v) / len(v))

			yield (user_id, item_id, rating)


	def _neighbors(self, user, allusers):
		""" Get neighbors of user.
		Criteria is set by heuristic, which cosine similarity is more than 0.35
		:param user: Dictionary value that has { item_id: rating } set
		:return: List of users
		"""
		ret = []
		for candidate in allusers:
			if user == candidate:
				continue
			if self._sim(user, candidate) >= 0.35:
				ret.append(candidate)

		return ret


	def _sim(self, user1, user2):
		""" Get similarity between user1 and user2 (Cosine)
		:param user1: Dictionary value that has { item_id: rating } set
		:param user2: Dictionary value that has { item_id: rating } set
		:return: Similarity calculated by cosine similarity (0~1)
		"""
		# list of (rating1, rating2)
		v = [(rating1, user2.get(item_id, 0)) for item_id, rating1 in user1.items()]

		if len(v) == 0:
			return 0
		elif sum([w1 * w2 for w1, w2 in v]) == 0:
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
	test_file_name = sys.argv[2]

	print('Build model.. please wait')
	rc = Recommender(
		Recommender.file2dataset(open(training_file_name, 'r')),
		Recommender.file2dataset(open(test_file_name, 'r')),
	)

	output_filename = training_file_name.split('.')[0] + '.base_prediction.txt'
	print('Writing predicated data to %s ...' % output_filename)

	with open(output_filename, 'w') as output_file:
		for user_id, item_id, rating in rc.predicate():
			output_file.write('%d\t%d\t%s\n' % (user_id, item_id, rating))

	print('Yeah! Finished')
