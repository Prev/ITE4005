from clustering import Cluster, Point


def test_point_dist():
	""" Unit Test of Point.dist()
	"""
	p1 = Point(1, 3.0, 4.0)
	p2 = Point(2, 0.0, 0.0)

	assert p1.dist(p2) == 5
	assert p2.dist(p1) == 5


sample_points = [
	Point(0, 0, 0), Point(1, 0, 1), Point(2, 0, 5),
	Point(3, 1, 0), Point(4, 1, 1), Point(5, 1, 5),
	Point(6, 2, 0), Point(7, 2, 1), Point(8, 6, 0),
	Point(9, 6, 1), Point(10, 6, 2), Point(11, 6, 3),
	Point(12, 7, 0), Point(13, 7, 1), Point(14, 7, 2),
	Point(15, 7, 3),
]


def test_neighbors():
	""" Unit Test of Cluster._neighbors()
	"""
	c = Cluster(sample_points, 2, 1, 3)
	assert c._neighbors(sample_points[0]) == [sample_points[1], sample_points[3]]

	c = Cluster(sample_points, 2, 1.5, 3)
	assert c._neighbors(sample_points[0]) == [sample_points[1], sample_points[3], sample_points[4]]


def test_cluster():
	""" Test of Cluster.clusters()
	"""
	c = Cluster(sample_points, 2, 1, 3)

	found = c.clusters()
	cluster1 = [0, 1, 3, 4, 6, 7]
	cluster2 = [8, 9, 10, 11, 12, 13, 14, 15]
	assert (found == [cluster1, cluster2]) or (found == [cluster2, cluster1])