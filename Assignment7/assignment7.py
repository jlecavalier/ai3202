def cleanup_samples(samples):
  new_samples = []

  for i in range(25):
    c = samples[i*4] < .5
    s = (c and samples[(i*4)+1] < .1) or (not c and samples[(i*4)+1] < .5)
    r = (c and samples[(i*4)+2] < .8) or (not c and samples[(i*4)+2] < .2)
    w = (s and r and samples[(i*4)+3] < .99) or (s and not r and samples[(i*4)+3] < .9) or (not s and r and samples[(i*4)+3] < .9) or (not s and not r and samples[(i*4)+3] < 0)
    new_samples.append([c,s,r,w])

  print(new_samples)
  return new_samples

def probabilities(pc,ps,pr,pw):
  p1 = pc

  num = .8 * .5
  den = (.8 * .5) + (.2 * .5)
  p2 = num / den

  num = ps * ((.9 * (1 - pr)) + (.99 * pr))
  den = pw
  p3 = num / den

  pwgs = (.99 * pr) + (.9 * (1-pr))
  pwgns = (.9 * pr)
  num = (pwgs * ps)
  den = (pwgs * ps) + (pwgns * (1 - ps))
  p4 = .1 + (num / den)

  return [p1,p2,p3,p4]

def direct_method():
  pc = .5
  ps = ((.5 * .1) + (.5 * .5))
  pr = ((.5 * .8) + (.5 * .2))
  pw = (.99 * ps * pr) + (.9 * ps * (1 - pr)) + (.9 * (1 - ps) * pr)

  probs = probabilities(pc,ps,pr,pw)

  print("\nCOMPUTING PROBABILITIES DIRECTLY:\n")
  print("P(C) = %.4f" % probs[0])
  print("P(C|R) = %.4f" % probs[1])
  print("P(S|W) = %.4f" % probs[2])
  print("P(S|C,W) = %.4f" % probs[3])

  return probs

def prior_sampling(samples):
  pc_t = [x for x in samples if x[0]]
  p1 = float(len(pc_t)) / 25.0

  pr_t = [x for x in samples if x[2]]
  pc_tgr = [x for x in pr_t if x[0]]
  p2 = float(len(pc_tgr)) / float(len(pr_t))

  pw_t = [x for x in samples if x[3]]
  ps_tgw = [x for x in pw_t if x[1]]
  p3 = float(len(ps_tgw)) / float(len(pw_t))

  pwc = [x for x in samples if (x[3] and x[0])]
  psgwc = [x for x in pwc if x[1]]
  p4 = float(len(psgwc)) / float(len(pwc))

  print("\nCOMPUTING PROBABILITIES VIA PRIOR SAMPLING:\n")
  print("P(C) = %.4f" % p1)
  print("P(C|R) = %.4f" % p2)
  print("P(S|W) = %.4f" % p3)
  print("P(S|C,W) = %.4f" % p4)

  return [p1,p2,p3,p4]

if __name__ == '__main__':
  # Get the samples
  sf = open('samples.dat')
  samples = sf.readlines()
  for i in range(len(samples)):
  	samples[i] = float(samples[i])
  sf.close()

  samples = cleanup_samples(samples)

  direct = direct_method()

  prior = prior_sampling(samples)