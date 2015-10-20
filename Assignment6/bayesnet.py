import argparse
import itertools

def handle_p(p):
	assert ((len(p) == 2) or (len(p) == 4)), "\nThere should be exactly 2 or 4 arguments provided for option -p. You provided %d...\n" % len(p)
	assert p[0] == 'p' or p[0] == 's' or p[0] == '~p' or p[0] == '~s', "\nFirst argument for option -p should be p/~p for pollution or s/~s for smoker. You chose %s...\n" % p[0]
	assert float(p[1]) >= 0 and float(p[1]) <= 1, "\nSecond argument for option -p should be a float between 0 and 1. Yours is %.4f...\n" % float(p[1])
	if len(p) == 2:
		if p[0] == 'p':
			return (float(p[1]),.3)
		elif p[0] == '~p':
			return (1.0-float(p[1]),.3)
		elif p[0] == '~s':
			return (.9,1.0-float(p[1]))
		else:
			return (.9,float(p[1]))
	else:
		assert float(p[3]) >= 0 and float(p[3]) <= 1, "\nFourth argument for option -p should be a float between 0 and 1. Yours is %.4f...\n" % float(p[3])
		assert p[0] != p[2], "\nYou can't set the prior value for p or s twice!\n"
		assert not (p[0] == 'p' and p[2] == '~p') and not (p[0] == '~p' and p[2] == 'p'), "\nYou can't set the prior value for p and ~p\n"
		assert not (p[0] == 's' and p[2] == '~s') and not (p[0] == '~s' and p[2] == 's'), "\nYou can't set the prior value for s and ~s\n"
		if p[0] == 'p' and p[2] == 's':
			return (float(p[1]),float(p[3]))
		elif p[0] == 'p' and p[2] == '~s':
			return (float(p[1]),1.0-float(p[3]))
		elif p[0] == '~p' and p[2] == 's':
			return (1.0-float(p[1]),float(p[3]))
		else:
			return (1.0-float(p[3]),1.0-float(p[1]))

class Node:
	def __init__(self,label):
		self.label = label
		self.probability = 0.0
		self.parents = []
		self.children = []

	def add_parent(self,newparent):
		self.parents.append(newparent)

	def add_child(self,newchild):
		self.children.append(newchild)

	def set_probability(self,prior):
		self.probability = prior

	def get_probability(self):
		if len(self.parents) > 0:
			parent_probabilities = []
			for parent in self.parents:
				parent_probabilities.append([parent.probability,1.0-parent.probability])
			cprod = list(itertools.product(*parent_probabilities))
			print(cprod)
			bigsum = 0
			for ii in cprod:
				tprod = 1
				for i in ii:
					tprod = tprod * i
				bigsum += tprod
			self.probability = bigsum

def generate_bnet(priors):
	pollution = Node("pollution")
	pollution.set_probability(priors[0])

	smoker = Node("smoker")
	smoker.set_probability(priors[1])

	cancer = Node("cancer")
	cancer.add_parent(pollution)
	cancer.add_parent(smoker)
	cancer.get_probability()
	print(cancer.probability)

	dyspnoea = Node("dyspnoea")
	dyspnoea.add_parent(cancer)
	cancer.add_child(dyspnoea)
	dyspnoea.get_probability()

	xray = Node("xray")
	xray.add_parent(cancer)
	cancer.add_child(xray)
	xray.get_probability

if __name__ == "__main__":
	argparser = argparse.ArgumentParser()
	argparser.add_argument("-p", nargs='+', help="prior values for pollution and smoker", default=("p", .9, "s", .3), required=False)

	args = argparser.parse_args()
	p = handle_p(args.p)
	print(p)

	bnet = generate_bnet(p)