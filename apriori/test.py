p = open('input.txt', 'r')

cnt = 0
total = 0
for line in p.readlines() :
	line = line[0:-1]
	l = line.split('\t')

	if '0' in l and '1' in l and '2' in l :
		cnt += 1
	total += 1

print(cnt)
print(total)
print(cnt / total)