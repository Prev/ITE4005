import dy


def test_info():
	assert (dy.DecisionTree.info(9, 5) - 0.94) <= 0.001


def test_tree():
	dt = dy.DecisionTree(open('../data/dt_train.txt'))
	assert dt.tree[0] == 'age'

	assert dt.tree[1]['<=30'][0] == 'student'
	assert dt.tree[1]['<=30'][1]['yes'] == 'yes'
	assert dt.tree[1]['<=30'][1]['no'] == 'no'

	assert dt.tree[1]['31...40'] == 'yes'

	assert dt.tree[1]['>40'][0] == 'credit_rating'
	assert dt.tree[1]['>40'][1]['excellent'] == 'no'
	assert dt.tree[1]['>40'][1]['fair'] == 'yes'


def test_testing():
	dt = dy.DecisionTree(open('../data/dt_train.txt'))
	assert dt.test({
		'age': '<=30',
		'income': 'low',
		'student': 'no',
		'credit_rating': 'fair',
	}) == 'no'
