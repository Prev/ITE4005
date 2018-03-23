import sys

def itemset_hash(itemset) :
	return ','.join(str(x) for x in itemset)

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
			if line[-1] == '\n': line = line[0:-1]
			t = line.split('\t')

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

		#####
		# Get association rules
		#####
		rules = self.all_association_rules(
			*self.get_itemsets_and_supports()
		)

		#####
		# Save association rules
		#####
		for itemset, ass_itemset, sup, conf in rules :
			output_file.write("%s\t%s\t%.2f\t%.2f\n" % (
				self.pretty_itemset(itemset),
				self.pretty_itemset(ass_itemset),
				sup / len(self.transactions) * 100,
				conf * 100,
			))

		print("%d2 rules are created" % len(rules))


	def get_itemsets_and_supports(self):
		""" Get frequent itemsets by apriori algorithm
		"""
		frequent_itemsets = []
		frequent_supports = []

		itemsets = [[i] for i in range(0, len(self.item_list))]
		k = 0
		while True :
			supports = self._calc_supports(itemsets)
			cur_frequent_itemsets, cur_frequent_supports = self._get_frequent_itemsets_and_supports(itemsets, supports)

			frequent_itemsets += cur_frequent_itemsets
			frequent_supports += cur_frequent_supports

			candidates = self._get_candidates(cur_frequent_itemsets, k+1)

			#self._print_itemsets(itemsets, supports)

			if len(candidates) == 0 :
				break
			else :
				itemsets = candidates
				k += 1

		return frequent_itemsets, frequent_supports

	def all_association_rules(self, frequent_itemsets, supports) :
		"""
		Get all association rules from itemsets
		:param frequent_itemsets: List of itemsets
		:return: List of tuple(itemset, associative_itemset, support, confidence)
		"""
		support_table = {}
		for i in range(0, len(frequent_itemsets)):
			support_table[itemset_hash(frequent_itemsets[i])] = supports[i]

		ret = []

		def recurs(mset):
			flag = [0] * len(mset)

			def powerset(depth):
				if len(mset) <= 1:
					return

				if depth == len(mset):
					p_set = []
					q_set = []

					for i in range(0, depth):
						if flag[i]: p_set.append(mset[i])
						else:       q_set.append(mset[i])

					if len(p_set) == 0 or len(q_set) == 0:
						return

					tmp = support_table[itemset_hash(sorted(set(p_set) | set(q_set)))]
					sup = tmp
					conf = tmp / support_table[itemset_hash(p_set)]

					ret.append((p_set, q_set, sup, conf))

					return

				flag[depth] = 1
				powerset(depth + 1)

				flag[depth] = 0
				powerset(depth + 1)

			powerset(0)

		for itemset in frequent_itemsets:
			recurs(itemset)

		return ret

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

	def _get_frequent_itemsets_and_supports(self, itemsets, supports):
		""" Get frequent itemsets by condition `minimum_support`

		:param itemsets: List of itemset
		:param supports: List or support value returned from `_calc_supports`
		:return: Tuple of (List of itemset) and (List of support)
		"""
		ret_itemsets = []
		ret_supports = []

		for i, itemset in enumerate(itemsets):
			if self._satisfying_support(supports[i]):
				ret_itemsets.append(itemset)
				ret_supports.append(supports[i])

		return (ret_itemsets, ret_supports)

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
					candidates.append(sorted(set(itemset1) | set(itemset2)))

		return candidates

	def _satisfying_support(self, support):
		""" Return whether this value satisfying condition

		:param support: Number
		:return: Boolean
		"""
		return (support / len(self.transactions)) >= self.minimum_support

	def _print_itemsets(self, itemsets, supports):
		""" Print itemsets and supports for debug
		"""
		print("---------------")
		for i, itemset in enumerate(itemsets) :
			print("%s: %.2f <%s>" % (
				self.pretty_itemset(itemset),
				supports[i] / len(self.transactions) * 100,
				'Yes' if self._satisfying_support(supports[i]) else 'No',
			))

		print("---------------")

	def pretty_itemset(self, itemset):
		""" Get string version of itemset like {0,1,4}
		"""
		return "{%s}" % ','.join(sorted(
			[self.item_list[x] for x in itemset]
		))


if __name__ == '__main__':
	if len(sys.argv) != 4:
		print("Usage: python apriori.py <minimum_support> <input_file> <output_file>")
		sys.exit(-1)

	Apriori(
		int(sys.argv[1]) / 100,
		open(sys.argv[2], 'r'),
		open(sys.argv[3], 'w'),
	)
