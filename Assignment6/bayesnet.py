import argparse

def handle_p(p):
	assert ((len(p) == 2) or (len(p) == 4)), "\nThere should be exactly 2 or 4 arguments provided for option -p. You provided %d...\n" % len(p)
	assert p[0] == 'p' or p[0] == 's', "\nFirst argument for option -p should be p for pollution or s for smoker. You chose %s...\n" % p[0]
	assert float(p[1]) >= 0 and float(p[1]) <= 1, "\nSecond argument for option -p should be a float between 0 and 1. Yours is %.4f...\n" % float(p[1])
	if len(p) == 2:
		if p[0] == 'p':
			return (float(p[1]),.3)
		else:
			return (.9,float(p[1]))
	else:
		assert p[0] != p[2], "\nYou can't set the prior value for p or s twice!\n"
		if p[0] == 'p':
			return (float(p[1]),float(p[3]))
		else:
			return (float(p[3]),float(p[1]))

def handle_args(args):
	p = handle_p(args.p)
	return p

if __name__ == "__main__":
	argparser = argparse.ArgumentParser()
	argparser.add_argument("-p", nargs='+', help="prior values for pollution and smoker", default=("p", .9, "s", .3), required=False)

	args = argparser.parse_args()
	p = handle_args(args)
	print(p)
	#print(args.p[0][1])
	#world = matrix_of_file(open(args.f))
