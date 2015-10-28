import argparse, itertools, getopt, sys

def calcMarginal(bnet, m):
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
	priors = [0.9,0.3]
	print("Hello?")

	try:
		opts, args = getopt.getopt(sys.argv[1:], "m:g:j:p:")
		for o, a in opts:
			if o in ("-p"):
				print "flag", o
				print "args", a
				print a[0]
				print float(a[1:])
				if a[0] == "P" or a[0] == "p":
					priors[0] = float(a[1:])
				elif a[0] == "S" or a[0] == "s":
					priors[1] = float(a[1:])
				bnet = generate_bnet(priors)
			elif o in ("-m"):
				print "flag", o
				print "args", a
				print type(a)
				calcMarginal(bnet, a)
			elif o in ("-g"):
				print "flag", o
				print "args", a
				print type(a)
				'''you may want to parse a here and pass the left of |
				and right of | as arguments to calcConditional
				'''
				p = a.find("|")
				print a[:p]
				print a[p+1:]
				#calcConditional(a[:p], a[p+1:])
			elif o in ("-j"):
				print "flag", o
				print "args", a
			else:
				assert False, "unhandled option"

	except getopt.GetoptError as err:
		# print help information and exit:
		print str(err) # will print something like "option -a not recognized"
        sys.exit(2)