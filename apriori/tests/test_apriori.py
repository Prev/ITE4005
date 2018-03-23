from io import StringIO
import apriori

def test_apriori():
	input_file = open('tests/test_input.txt', 'r')
	output = StringIO()

	ap = apriori.Apriori(0.2, input_file, output)

	contents = output.getvalue()
	print(contents)

	ret_max = {}

	for line in contents.split("\n") :
		if not len(line) :
			continue

		p, q, sup, conf = line.split("\t")
		print("%s/%s/%s/%s" % (p, q, sup, conf))

		ret_max['%s->%s' % (p, q)] = (sup, conf)

	assert ret_max['{Ramen,Tuna}->{Egg}']  == ('20.00', '100.00')
	assert ret_max['{Tuna}->{Egg}'] == ('20.00', '100.00')
	assert ret_max['{Tuna}->{Egg,Ramen}'] == ('20.00', '100.00')
	assert ret_max['{Ramen}->{Egg}'] == ('40.00', '50.00')
	assert ret_max['{Ramen}->{Coke}'] == ('40.00', '50.00')
	assert ret_max['{Egg}->{Coke}'] == ('30.00', '60.00')

