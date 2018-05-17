"""
@author Prev (prevdev@gmail.com)
"""
import sys
import math

class Point:
	class Label:
		UNCLASSIFIED = 0
		NOISE = -1

	def __init__(self, id, x, y):
		""" Point Constructor
		:param id: ID of point
		:param x: X-axis position
		:param y: Y-axis position
		"""
		self.id = id
		self.x = x
		self.y = y
		self.cluster = Point.Label.UNCLASSIFIED

	def dist(self, target):
		""" Euclidean distance with other point
		:param target: Point instance
		:return: Numeric distance
		"""
		return math.sqrt(math.pow(self.x - target.x, 2) + math.pow(self.y - target.y, 2))


class Cluster:

	@staticmethod
	def file2points(input_file):
		""" Read file and interpret to list of Points
		:param input_file: Opened file
		:return: List of Point
		"""
		ret = []
		for line in input_file.readlines():
			if line[-1] == '\n': line = line[0:-1]
			t = line.split('\t')

			ret.append(Point(
				id=int(t[0]),
				x=float(t[1]),
				y=float(t[2])
			))

		return ret

	def __init__(self, points, n, esp, minpts):
		""" Initialize Cluster
		:param points: List of Point class
		:param n: Number of clusters
		:param esp: Epsilon of DBScan
		:param minpts: MinPts of DBScan
		"""
		self.points = points
		self.n = n
		self.esp = esp
		self.minpts = minpts

	def clusters(self):
		""" Get clusters by running DBScan
		:return: List of clusters (Cluster is list of point ids)
		"""
		print('Start clustering...')

		cluster_id = 1
		for point in self.points:
			if point.cluster != Point.Label.UNCLASSIFIED:
				continue

			# Get neighbors of current point
			neighbors = self._neighbors(point)

			# If it has not enough neighbors, set it as noise
			if len(neighbors) < self.minpts:
				point.cluster = Point.Label.NOISE
				continue

			# Else if it is core point, make cluster and expand
			# to find more points that belong to same cluster
			point.cluster = cluster_id
			self._expand(
				seeds=neighbors,
				cluster_id=cluster_id
			)
			cluster_id += 1

		# Make cluster list from points
		clusters = [[] for _ in range(0, cluster_id-1)]
		for point in self.points:
			if point.cluster == Point.Label.NOISE:
				continue
			clusters[point.cluster - 1].append(point.id)

		clusters.sort(key=lambda l: len(l), reverse=True)
		return clusters[0:self.n]

	def _neighbors(self, point):
		""" Get neighbors of point
		:param point: The point to find out neighbors
		:return: List of points
		"""
		return [p for p in self.points if p != point and point.dist(p) <= self.esp]

	def _expand(self, seeds, cluster_id):
		""" Expand candidate points for clustering
		:param seeds: Seed for performing expansion
		:param cluster_id: If new point is same cluster to seed, set its cluster to this
		"""
		for point in seeds:
			if point.cluster == Point.Label.NOISE:
				point.cluster = cluster_id

			if point.cluster == Point.Label.UNCLASSIFIED:
				point.cluster = cluster_id
				n_neighbors = self._neighbors(point)
				if len(n_neighbors) >= self.minpts:
					seeds.extend(n_neighbors)


if __name__ == '__main__':
	if len(sys.argv) != 5:
		print("Usage: python cluster.py <input_file> <n> <esp>, <minpts>")
		sys.exit(-1)

	input_file_name = sys.argv[1]

	c = Cluster(
		Cluster.file2points(open(input_file_name, 'r')),
		int(sys.argv[2]),
		int(sys.argv[3]),
		int(sys.argv[4]),
	)

	for index, output in enumerate(c.clusters()):
		output_filename = input_file_name.split('.')[0] + '_cluster_%d.txt' % index

		with open(output_filename, 'w') as output_file:
			for object_id in output:
				output_file.write('%d\n' % object_id)

		print('Result of cluster %d is written in "%s"' % (index, output_filename))
