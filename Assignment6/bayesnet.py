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

def handle_m(bnet, m):
	for i in m:
		assert i == 'p' or i == 's' or i == 'c' or i == 'd' or i == 'x' \
		or i == '~p' or i == '~s' or i == '~c' or i == '~d' or i == '~x' \
		or i == 'P' or i == 'S' or i == 'C' or i == 'D' or i == 'X' \
		or i == '~P' or i == '~S' or i == '~C' or i == '~D' or i == '~X', \
		"\nThere is no variable designated by %s\n" % i
		if i == 'p' or i == 'P':
			print("\nMarginal probability of low pollution: %.4f\n" % bnet[0].probability)
		elif i == 's' or i == 'S':
			print("\nMarginal probability of being a smoker: %.4f\n" % bnet[1].probability)
		elif i == 'c' or i == 'C':
			print("\nMarginal probability of having cancer: %.4f\n" % bnet[2].probability)
		elif i == 'd' or i == 'D':
			print("\nMarginal probability of dyspnoea: %.4f\n" % bnet[3].probability)
		elif i == 'x' or i == 'X':
			print("\nMarginal probability of xray being positive: %.4f\n" % bnet[4].probability)
		elif i == '~p' or i == '~P':
			print("\nMarginal probability of high pollution: %.4f\n" % (1 - bnet[0].probability))
		elif i == '~s' or i == '~S':
			print("\nMarginal probability of not being a smoker: %.4f\n" % (1 - bnet[1].probability))
		elif i == '~c' or i == '~C':
			print("\nMarginal probability of not having cancer: %.4f\n" % (1 - bnet[2].probability))
		elif i == '~d' or i == '~D':
			print("\nMarginal probability of not having dyspnoea: %.4f\n" % (1 - bnet[3].probability))
		elif i == '~x' or i == '~X':
			print("\nMarginal probability of xray being negative: %.4f\n" % (1 - bnet[4].probability))

def prob_of_string(bnet, s):
	if s == 'p':
		return bnet[0].probability
	elif s == 's':
		return bnet[1].probability
	elif s == 'c':
		return bnet[2].probability
	elif s == 'd':
		return bnet[3].probability
	elif s == 'x':
		return bnet[4].probability

def cond_prob(bnet,query,observed):
	if query == "p":
		node = bnet[0]
	elif query == "s":
		node = bnet[1]
	elif query == "c":
		node = bnet[2]
	elif query == "d":
		node = bnet[3]
	elif query == "x":
		node = bnet[4]
	if observed in node.cprobs:
		return node.cprobs[observed]
	else:
		return joint_prob(bnet,query,observed) / prob_of_string(bnet, observed)

def joint_prob(bnet,e1,e2):
	return cond_prob(e1,e2) * prob_of_string(bnet, e2)

class Node:
	def __init__(self,label):
		self.label = label
		self.probability = 0.0
		self.cprobs = {}

	def set_probability(self,prior):
		self.probability = prior

	def set_cond_prob(self,s,prob):
		self.cprobs[s] = prob

def generate_bnet(priors):
	# Probability of low pollution was given
	pollution = Node("pollution")
	pollution.set_probability(priors[0])
	pollution.set_cond_prob("s",pollution.probability)

	# Probability for smoker was given.
	smoker = Node("smoker")
	smoker.set_probability(priors[1])
	smoker.set_cond_prob("p",smoker.probability)

	# Set probability for cancer.
	cancer = Node("cancer")
	cancer.set_cond_prob("~p,s",.05)
	cancer.set_cond_prob("~p,~s",.02)
	cancer.set_cond_prob("p,s",.03)
	cancer.set_cond_prob("p,~s",.001)
	x1 = (1 - pollution.probability) * smoker.probability * cancer.cprobs["~p,s"]
	x2 = (1 - pollution.probability) * (1 - smoker.probability) * cancer.cprobs["~p,~s"]
	x3 = pollution.probability * smoker.probability * cancer.cprobs["p,s"]
	x4 = pollution.probability * (1 - smoker.probability) * cancer.cprobs["p,~s"]
	cancer.set_probability(x1+x2+x3+x4)

	# Set probability for dyspnoea
	dyspnoea = Node("dyspnoea")
	dyspnoea.set_cond_prob("c",.65)
	dyspnoea.set_cond_prob("~c",.3)
	x1 = cancer.probability * dyspnoea.cprobs["c"]
	x2 = (1 - cancer.probability) * dyspnoea.cprobs["~c"]
	dyspnoea.set_probability(x1+x2)
	dyspnoea.set_cond_prob("x",dyspnoea.probability)

	# Set probability for xray
	xray = Node("xray")
	xray.set_cond_prob("c",.9)
	xray.set_cond_prob("~c",.2)
	x1 = cancer.probability * xray.cprobs["c"]
	x2 = (1 - cancer.probability) * xray.cprobs["~c"]
	xray.set_probability(x1+x2)
	xray.set_cond_prob("d",xray.probability)

	return [pollution,smoker,cancer,dyspnoea,xray]

if __name__ == "__main__":
	argparser = argparse.ArgumentParser()
	argparser.add_argument("-p", nargs='+', help="prior values for pollution and smoker", default=("p", .9, "s", .3), required=False)
	argparser.add_argument("-m", nargs='*', help="marginal probability for a variable", default="", required=False)

	args = argparser.parse_args()
	p = handle_p(args.p)

	bnet = generate_bnet(p)

	handle_m(bnet,args.m)