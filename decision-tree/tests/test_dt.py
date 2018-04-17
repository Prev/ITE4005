from dt import DecisionTree


def test_info():
	assert (DecisionTree.info(9, 5) - 0.94) <= 0.001


def test_tree():
	dt = DecisionTree(open('data/dt_train.txt'))
	assert dt.tree[0] == 'age'

	assert dt.tree[1]['<=30'][0] == 'student'
	assert dt.tree[1]['<=30'][1]['yes'] == 'yes'
	assert dt.tree[1]['<=30'][1]['no'] == 'no'

	assert dt.tree[1]['31...40'] == 'yes'

	assert dt.tree[1]['>40'][0] == 'credit_rating'
	assert dt.tree[1]['>40'][1]['excellent'] == 'no'
	assert dt.tree[1]['>40'][1]['fair'] == 'yes'


def test_majority_voting():
	dt = DecisionTree(open('tests/one_attr.txt'))

	assert dt.tree[1]['<=30'] == 'no'
	assert dt.tree[1]['31...40'] == 'yes'
	assert dt.tree[1]['>40'] == 'yes'


def test_test():
	dt = DecisionTree(open('data/dt_train.txt'))
	assert dt.test({
		'age': '<=30',
		'income': 'low',
		'student': 'no',
		'credit_rating': 'fair',
	}) == 'no'


def test_testfile():
	from io import StringIO

	dt = DecisionTree(open('data/dt_train.txt'))
	output = StringIO()
	dt.testfile(open('data/dt_test.txt'), output)

	contents = output.getvalue()

	for line in contents.split("\n"):
		if not len(line):
			continue

		last_elm = line.split("\t")[-1]
		assert last_elm in ('Class:buys_computer', 'yes', 'no')
