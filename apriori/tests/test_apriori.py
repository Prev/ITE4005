from io import StringIO
import apriori

def _test(minimum_support):
	input_file = open('input.txt', 'r')
	output = StringIO()
	compare = open('tests/outputRsupport%d.txt' % minimum_support, 'r')

	apriori.Apriori(0.01 * minimum_support, input_file, output)

	contents = output.getvalue()
	ret_matrix = {}

	for line in contents.split("\n"):
		if not len(line):
			continue

		p, q, sup, conf = line.split("\t")
		ret_matrix['%s->%s' % (p, q)] = (sup, conf)


	for line in compare.readlines():
		if line[-1] == '\n': line = line[0:-1]

		p, q, sup, conf = line.split("\t")
		assert ret_matrix['%s->%s' % (p, q)] == (sup, conf)

		# key = '%s->%s' % (p, q)
		# if key not in ret_matrix:
		# 	print("No key:\t", line)
		#
		# elif ret_matrix[key] != (sup, conf):
		# 	print("Mismatched:\t", key)
		# 	print("\t\t\t Expected:  ", (sup, conf))
		# 	print("\t\t\t Real:\t\t", ret_matrix[key])



	compare.close()


def test_minimum_support4():
	_test(4)


def test_minimum_support5():
	_test(5)
