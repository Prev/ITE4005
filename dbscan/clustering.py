"""
@author Prev (prevdev@gmail.com)
"""
import sys
import math


class Cluster:
	def __init__(self, input_file, n, esp, minpts):
		""" Initialize Cluster
		"""
		pass

	def clusters(self):
		return []


if __name__ == '__main__':
	if len(sys.argv) != 5:
		print("Usage: python cluster.py <input_file> <n> <esp>, <minpts>")
		sys.exit(-1)

	input_file_name = sys.argv[1]

	c = Cluster(
		open(input_file_name, 'r'),
		int(sys.argv[2]),
		int(sys.argv[3]),
		int(sys.argv[4]),
	)

	for index, output in enumerate(c.clusters()):
		with open(input_file_name + '_cluster_%d.txt' % index, 'w') as output_file:
			for object_id in output:
				output_file.write('%d\n', object_id)
