import sys

if len(sys.argv) != 4:
	print("Usage: python apriori.py 5 input.txt output")
	sys.exit(-1)


class Apriori:

	# 2d list of item (list of transactions)
	transactions = []

	# Set of transaction items
	item_list = set()

	# Matrix consisted by 0 or 1
	sparse_matrix = []

	def __init__(self, minimum_support, input_file, output_file):
		""" Initialize apriori

		:param minimum_support: ex) 5 -> 5%
		:param input_file: Opened file object to read
		:param output_file: Opened file object to write
		"""
		self.minimum_support = minimum_support

		for line in input_file.readlines() :
			t = line[0:-1].split("\t") # Remove '\n' on end of string and split it

			self.transactions.append(t)
			self.item_list |= set(t) # Add new item ids

		self.item_list = list(self.item_list) # Fix order


		#####
		# Build sparse matrix
		#####
		id_of_item = dict(zip(self.item_list, range(0, len(self.item_list))))

		for transaction in self.transactions:
			self.sparse_matrix.append([0] * len(self.item_list))

			for item in transaction:
				self.sparse_matrix[-1][id_of_item[item]] = 1

		self._run()



	def _run(self):
		""" Run algorithm
		"""
		itemsets = []
		for i in range(0, len(self.item_list)):
			itemsets.append([i])

		k = 0
		while True :
			supports = self._calc_supports(itemsets)
			frequent_itemsets = self._get_frequent_itemsets(itemsets, supports)

			self._print_itemsets(itemsets, supports)

			candidates = self._get_candidates(frequent_itemsets, k+1)

			if len(candidates) == 0 :
				break
			else :
				itemsets = candidates
				k += 1

	def _calc_supports(self, itemsets):
		""" Calculate supports by itemsets

		:param itemsets: List of itemset
		:return: List or support value of each itemset
		"""
		supports = [0] * len(itemsets)

		for row in self.sparse_matrix:
			for no, itemset in enumerate(itemsets):
				exists = True
				for item_id in itemset:
					if not row[item_id]:
						exists = False
						break

				if exists:
					supports[no] += 1

		return supports

	def _get_frequent_itemsets(self, itemsets, supports):
		""" Get frequent itemsets by condition `minimum_support`

		:param itemsets: List of itemset
		:param supports: List or support value returned from `_calc_supports`
		:return: List of itemset
		"""
		new_itemsets = []

		for i, itemset in enumerate(itemsets):
			if self._satisfying_support(supports[i]):
				new_itemsets.append(itemset)

		return new_itemsets

	def _get_candidates(self, itemsets, k):
		""" Get candidates on next step

		:param itemsets: List of itemset
		:param k: Step number
		:return: List of itemset
		"""
		candidates = []
		for i in range(0, len(itemsets)):
			for j in range(i + 1, len(itemsets)):
				itemset1 = itemsets[i]
				itemset2 = itemsets[j]

				valid = True
				for l in range(0, k - 1):
					if itemset1[l] != itemset2[l]:
						valid = False
						break

				if not itemset1[k - 1] < itemset2[k - 1]:
					valid = False

				if valid:
					candidates.append(list(set(itemset1) | set(itemset2)))

		return candidates

	def _satisfying_support(self, support):
		""" Return whether this value satisfying condition

		:param support: Number
		:return: Boolean
		"""
		return support / len(self.transactions) >= self.minimum_support

	def _print_itemsets(self, itemsets, supports):
		""" Print itemsets and supports for debug
		"""
		print("---------------")
		for i, itemset in enumerate(itemsets) :
			print("{%s}: %.2f" % (
				','.join(self.item_list[x] for x in itemset),
				supports[i] / len(self.transactions) * 100
			))

		print("---------------")


Apriori(
	int(sys.argv[1]) / 100,
	open(sys.argv[2], 'r'),
	open(sys.argv[3], 'w'),
)
