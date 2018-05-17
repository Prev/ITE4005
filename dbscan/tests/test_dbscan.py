from clustering import Cluster, Point

point_list1 = [
	Point(0, 0, 0), Point(1, 0, 1), Point(2, 0, 5),
	Point(3, 1, 0), Point(4, 1, 1), Point(5, 1, 5),
	Point(6, 2, 0), Point(7, 2, 1), Point(8, 6, 0),
	Point(9, 6, 1), Point(10, 6, 2), Point(11, 6, 3),
	Point(12, 7, 0), Point(13, 7, 1), Point(14, 7, 2),
	Point(15, 7, 3),
]


def test_point_dist():
	p1 = Point(1, 3.0, 4.0)
	p2 = Point(2, 0.0, 0.0)

	assert p1.dist(p2) == 5
	assert p2.dist(p1) == 5


def test_neighbors():
	c = Cluster(point_list1, 2, 1, 3)
	assert c._neighbors(point_list1[0]) == [point_list1[1], point_list1[3]]

	c = Cluster(point_list1, 2, 1.5, 3)
	assert c._neighbors(point_list1[0]) == [point_list1[1], point_list1[3], point_list1[4]]


def test_cluster():
	c = Cluster(point_list1, 2, 1, 3)
	assert c.clusters() == [[0, 1, 3, 4, 6, 7], [8, 9, 10, 11, 12, 13, 14, 15]]