import argparse, itertools, getopt, sys

def areIndependent(e1, e2):
	return (e1.label == "pollution" and e2.label == "smoker") \
		or (e1.label == "smoker" and e2.label == "pollution")

def stringToNode(bnet, s):
	if s == 'p' or s == 'P':
		return bnet[0]
	elif s == 's' or s == 'S':
		return bnet[1]
	elif s == 'c' or s == 'C':
		return bnet[2]
	elif s == 'd' or s == 'D':
		return bnet[3]
	elif s == 'x' or s == 'X':
		return bnet[4]

def calcMarginal(m):
	for i in m:
		print("\nMarginal probability of %s: %.4f\n" % (i.label, i.probability))

def calcConditional(e1,e2):
	if len(e2) == 1:
		if e1 == e2[0]:
			return 1.0
		elif areIndependent(e1,e2[0]):
			return e1.probability
		elif e1.label == "cancer" and e2[0].label == "smoker":
			p1 = .03 * e1.parents[0].probability
			p2 = .05 * (1 - e1.parents[0].probability)
			return p1 + p2
		elif e1.label == "cancer" and e2[0].label == "dyspnoea":
			num = .65 * e1.probability
			den = (.65 * e1.probability) + (.3 * (1 - e1.probability))
			return num/den
		elif e1.label == "cancer" and e2[0].label == "xray":
			num = .9 * e1.probability
			den = (.9 * e1.probability) + (.2 * (1 - e1.probability))
			return num/den
		elif e1.label == "pollution" and e2[0].label == "cancer":
			num = calcConditional(e2[0],[e1]) * e1.probability
			p1 = .05 * e2[0].parents[1].probability
			p2 = .02 * (1 - e2[0].parents[1].probability)
			pnot = p1 + p2
			den = (calcConditional(e2[0],[e1]) * e1.probability) + (pnot * (1 - e1.probability))
			return num/den
		elif e1.label == "pollution" and e2[0].label == "dyspnoea":
			num = calcConditional(e2[0],[e1]) * e1.probability
			psmoke = e2[0].parents[0].parents[1].probability
			p1 = .65 * ((psmoke * .05) + ((1-psmoke) * .02))
			p2 = .3 * ((psmoke * .95) + ((1-psmoke) * .98))
			pnot = p1 + p2
			den = (calcConditional(e2[0],[e1]) * e1.probability) + (pnot * (1 - e1.probability))
			return num/den
		elif e1.label == "smoker" and e2[0].label == "dyspnoea":
			num = calcConditional(e2[0],[e1]) * e1.probability
			ppol = e2[0].parents[0].parents[0].probability
			p1 = .65 * ((ppol * .001) + ((1-ppol) * .02))
			p2 = .3 * ((psmoke * .999) + ((1-ppol) * .98))
			pnot = p1 + p2
			den = (calcConditional(e2[0],[e1]) * e1.probability) + (pnot * (1 - e1.probability))
			return num/den
		else:
			return 0



class Node:
	def __init__(self,label):
		self.label = label
		self.probability = 0.0
		self.parents = []
		#self.depends = {}

	def set_probability(self,prior):
		self.probability = prior

def generate_bnet(priors):
	# Probability of low pollution was given
	pollution = Node("pollution")
	pollution.set_probability(priors[0])

	# Probability for smoker was given.
	smoker = Node("smoker")
	smoker.set_probability(priors[1])

	# Set probability for cancer.
	cancer = Node("cancer")
	cancer.parents = [pollution, smoker]
	x1 = (1 - pollution.probability) * smoker.probability * .05
	x2 = (1 - pollution.probability) * (1 - smoker.probability) * .02
	x3 = pollution.probability * smoker.probability * .03
	x4 = pollution.probability * (1 - smoker.probability) * .001
	cancer.set_probability(x1+x2+x3+x4)

	# Set probability for dyspnoea
	dyspnoea = Node("dyspnoea")
	dyspnoea.parents = [cancer]
	x1 = cancer.probability * .65
	x2 = (1 - cancer.probability) * .3
	dyspnoea.set_probability(x1+x2)

	# Set probability for xray
	xray = Node("xray")
	xray.parents = [cancer]
	x1 = cancer.probability * .9
	x2 = (1 - cancer.probability) * .2
	xray.set_probability(x1+x2)
	'''
	cancer.depends[[pollution, smoker]] = .03
	cancer.depends[[pollution]] = .001
	cancer.depends[[smoker]] = .05
	cancer.depends[[]] = .02

	dyspnoea.depends[cancer] = .65
	dyspnoea.depends[[]] = .3

	xray.depends[[cancer]] = .9
	xray.depends[[]] = .2
	'''
	return [pollution,smoker,cancer,dyspnoea,xray]

if __name__ == "__main__":
	
	# Default prior values
	priors = [0.9,0.3]

	try:
		opts, args = getopt.getopt(sys.argv[1:], "m:g:j:p:")
		if "-p" not in opts:
			bnet = generate_bnet(priors)
		for o, a in opts:
			if o in ("-p"):
				if a[0] == "P" or a[0] == "p":
					priors[0] = float(a[1:])
				elif a[0] == "S" or a[0] == "s":
					priors[1] = float(a[1:])
				bnet = generate_bnet(priors)
			elif o in ("-m"):
				a_prime = []
				for i in a:
					a_prime.append(stringToNode(bnet,i))
				calcMarginal(a_prime)
			elif o in ("-g"):
				'''you may want to parse a here and pass the left of |
				and right of | as arguments to calcConditional
				'''
				p = a.find("|")
				e1 = stringToNode(bnet,a[:p])
				e2 = []
				for i in a[p+1:]:
					e2.append(stringToNode(bnet,i))
				cp = calcConditional(e1, e2)
				s1 = e1.label
				s2 = e2[0].label
				for i in range(1,len(e2)):
					s2 = s2 + (", %s"%(e2[i].label))
				print("Conditional probability of %s given %s: %.4f" %(s1,s2,cp)) 
			else:
				assert False, "unhandled option"

	except getopt.GetoptError as err:
		# print help information and exit:
		print str(err) # will print something like "option -a not recognized"
        sys.exit(2)