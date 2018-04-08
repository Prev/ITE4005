"""
@author Prev (prevdev@gmail.com)
"""
import sys
import math

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

	def __init__(self, training_set, test_set, output_file) :
		""" Initialize apriori

		:param training_set: Opened file object to train
		:param test_set: Opened file object to tests
		:param output_file: Opened file object to write
		"""

		head = None
		table = {}
		rst = None
		dataset = []

		for line in training_set.readlines():
			if line[-1] == '\n': line = line[0:-1]
			t = line.split('\t')

			if head is None:
				# First line
				head = t

				for index, attr in enumerate(head):
					if index == len(t) - 1:
						# Do not calculate result column
						break

					table[attr] = {}
					for domain in self.DOMAINS[attr]:
						table[attr][domain] = {}
						for rst_domain in self.DOMAINS[head[-1]]:
							# Init table like `['age']['<=30']['yes']=0`
							table[attr][domain][rst_domain] = 0

			else:
				dataset.append(t)
				rst = t[-1]

				for index, data in enumerate(t):
					if index == len(t) - 1:
						# Do not calculate result column
						break

					table[head[index]][data][rst] += 1

		from pprint import pprint
		pprint(table)

		pprint(self.info(9, 5))

		for attr, D in table.items():
			infoA = sum([
				sum(Dj.values()) * self.info(*Dj.values()) for Dj in D.values()
			])
			# Sigma( |Dj| * Info(Dj) )

			print('Info.%s(D) = %s' % (attr, infoA))


	def info(self, *arg):
		""" Calculating Info(D) function

		:param *arg: List of tuple counts
		:return: Ranged value from 0 to 1
		"""

		s = sum(arg)
		ret = 0
		for a in arg:
			p = a/s
			if p == 0: continue
			ret += -(p * math.log(p, 2))
		return ret


if __name__ == '__main__':
	if len(sys.argv) != 4:
		print("Usage: python dt.py <training_set> <test_set> <output_file>")
		sys.exit(-1)

	DecisionTree(
		open(sys.argv[1], 'r'),
		open(sys.argv[2], 'r'),
		open(sys.argv[3], 'w'),
	)
