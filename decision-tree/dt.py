"""
@author Prev (prevdev@gmail.com)
"""
import sys
import math


def head_and_body(file):
	""" Read file and convert to (head, body) data

	:param file: Opened file stream
	:return: Tuple of (head, body)
	"""
	head = None
	body = []

	for line in file.readlines():
		if line[-1] == '\n': line = line[0:-1]
		t = line.split('\t')

		if head is None:
			# First line
			head = t
		else:
			body.append(t)

	return head, body



class DecisionTree :

	DOMAINS = {
		'age':    ('<=30', '31...40', '>40'),
		'income': ('high', 'medium', 'low'),
		'student': ('yes', 'no'),
		'credit_rating': ('fair', 'excellent'),
		'Class:buys_computer': ('yes', 'no'),

		'buying': ('vhigh', 'high', 'med', 'low'),
		'maint': ('vhigh', 'high', 'med', 'low'),
		'doors': ('2', '3', '4', '5more'),
		'persons': ('2', '4', 'more'),
		'lug_boot': ('small', 'med', 'big'),
		'safety': ('low', 'med', 'high'),
		'car_evaluation': ('unacc', 'acc', 'good', 'vgood'),
	}

	def __init__(self, training_set) :
		""" Initialize apriori

		:param training_set: Opened file object to train
		"""

		self.head, tuples = head_and_body(training_set)
		self.tree = self.maketree(self.head, tuples)


	def testfile(self, test_set, output_file=None):
		""" Test dataset in files

		:param test_set: Opened file object to tests
		:param output_file: Opened file object to write
		:return:
		"""
		n_head, tuples = head_and_body(test_set)

		output_file.write('\t'.join(self.head) + '\n')

		for tuple in tuples:
			d = {}
			for index, attr in enumerate(n_head):
				d[attr] = tuple[index]

			rst = self.test(d)
			output_file.write('%s\t%s\n' % ('\t'.join(tuple), rst))


	def test(self, data):
		""" Test data with trained data (tree)

		:param data: Dictionary data like {attr1: val1, attr2: val2, ...}
		:return: Predicted value of result attr
		"""
		cur = self.tree

		while type(cur) == tuple:
			# `cur` will be tuple if tree is remain (non-leaf)
			attr, rst = cur
			cur = rst[data[attr]]

		return cur


	def maketree(self, head, tuples):
		""" Make decision tree

		:param head: Attribute(class) set
		:param tuples: Data set
		:return: Tree used to decide something
				ex) ('age', {
						'31...40': 'yes',
					    '<=30': ('student', {'no': 'no', 'yes': 'yes'}),
					    '>40': ('credit_rating', {'excellent': 'no', 'fair': 'yes'})
					})
		"""
		if len(tuples) == 0:
			# There are no samples left
			return self.DOMAINS[head[-1]][0]

		result_vals = [row[-1] for row in tuples]

		if len(head) == 1:
			# There are no remaining attributes
			return max(set(result_vals), key=result_vals.count) # majority voting

		if result_vals.count(result_vals[0]) == len(result_vals):
			# All samples for a given node belong to the same class
			return result_vals[0]


		min_attr, data = self._highest_gain_attr(head, tuples)

		idx = head.index(min_attr)
		n_head = head[0:idx] + head[idx + 1:]

		ret = {}
		for domain, _tuples in data.items():
			n_tuples = [t[0:idx] + t[idx + 1:] for t in _tuples]
			ret[domain] = self.maketree(n_head, n_tuples)

		return (min_attr, ret)


	def _highest_gain_attr(self, head, tuples):
		""" Calculate Info and Gain value by tuples, and return highest gain attr and divided dataset

		:param head: Attribute(class) set
		:param tuples: Data set
		:return: Tuple<highest_gain_attr, divided dataset>
		"""
		cnt_table = {}
		data_table = {}

		for index, attr in enumerate(head):
			if index == len(head) - 1:
				# Do not calculate result column
				break

			cnt_table[attr] = {}
			data_table[attr] = {}

			if attr not in self.DOMAINS:
				print("Warning: Attribute '%s' is not able in this program" % attr)
				continue

			for domain in self.DOMAINS[attr]:
				cnt_table[attr][domain] = {}
				data_table[attr][domain] = []

				for rst_domain in self.DOMAINS[head[-1]]:
					# Init table like `['age']['<=30']['yes']=0`
					cnt_table[attr][domain][rst_domain] = 0

		for tuple in tuples:
			result_attr = tuple[-1]

			for index, data in enumerate(tuple):
				if index == len(tuple) - 1:
					# Ignore result column
					break

				cnt_table[head[index]][data][result_attr] += 1
				data_table[head[index]][data].append(tuple)


		candidates = []
		for attr, D in cnt_table.items():
			# Sigma( |Dj| * Info(Dj) ) / |D|
			infoA = sum([
				sum(Dj.values()) * DecisionTree.info(*Dj.values()) for Dj in D.values()
			]) / len(tuples)

			candidates.append((attr, infoA))

		min_attr = min(candidates, key=lambda x: x[1])[0]

		return min_attr, data_table[min_attr]


	@staticmethod
	def info(*arg):
		""" Calculating Info(D) function

		:param *arg: List of tuple counts
		:return: Ranged value from 0 to 1
		"""

		ret = 0
		s = sum(arg)
		if s == 0: return 0

		for a in arg:
			p = a/s
			if p == 0: continue
			ret += -(p * math.log(p, 2))
		return ret


if __name__ == '__main__':
	if len(sys.argv) != 4:
		print("Usage: python dt.py <training_set> <test_set> <output_file>")
		sys.exit(-1)

	dt = DecisionTree(open(sys.argv[1], 'r'))
	dt.testfile(
		open(sys.argv[2], 'r'),
		open(sys.argv[3], 'w'),
	)