def direct_method():
  pc = .5
  ps = ((.5 * .1) + (.5 * .5))
  pr = ((.5 * .8) + (.5 * .2))
  pw = (.99 * ps * pr) + (.9 * ps * (1 - pr)) + (.9 * (1 - ps) * pr)

  p1 = pc

  num = .8 * .5
  den = (.8 * .5) + (.2 * .5)
  p2 = num / den

  num = ps * ((.9 * (1 - pr)) + (.99 * pr))
  den = pw
  p3 = num / den

  print("P(C) = %.4f" % p1)
  print("P(C|R) = %.4f" % p2)
  print("P(S|W) = %.4f" % p3)

  return [p1,p2,p3]

if __name__ == '__main__':
  # Get the samples
  sf = open('samples.dat')
  samples = sf.readlines()
  for i in range(len(samples)):
  	samples[i] = float(samples[i])
  sf.close()

  direct = direct_method()