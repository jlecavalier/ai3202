from hmm import *
from math import log

def v1x1(o,hmm):
  res = []
  init = hmm.init_probs
  emis = [x for x in hmm.emis_probs if x[0][0] == o]
  assert len(init) == len(emis)
  for i in range(len(init)):
  	p = log(init[i][1]) + log(emis[i][1])
  	res.append(p)
  return res

def vtxt(o,emis,tran,v):
  res = []
  for i in range(len(v)):
  	i_tran = [x for x in tran if x[0][0] == chr(i+97)]
  	to_max = []
  	for j in range(len(i_tran)):
  	  p = log(emis[i][1]) + log(i_tran[j][1]) + v[j]
  	  to_max.append(p)
  	res.append(max(to_max))
  return res

def viterbi(obs,hmm):
  print("Running the viterbi algorithm. This may take quite a while...")
  v = [v1x1(obs[0],hmm)]
  emis = hmm.emis_probs
  tran = hmm.tran_probs
  for o in obs[1:]:
  	o_emis = [x for x in emis if x[0][0] == o]
  	v.append(vtxt(o,o_emis,tran,v[-1]))
  print("Done!")
  return v

def display_sequence(v):
  f = open('dump.data', 'w+')
  f2 = open('dump2.data', 'w+')
  for ii in v:
    f.write("%c" % chr(ii.index(max(ii))+97))
    f2.write("%.40f\n" % max(ii))

if __name__ == "__main__":
  (data,obs) = get_data_and_obs(open("typos20.data"))
  assert len(data) == len(obs)
  hmm = Hmm(data,obs)

  (t_data,t_obs) = get_data_and_obs(open("typos20Test.data"))
  t_data = t_data[1:]
  t_obs = t_obs[1:]
  assert len(t_data) == len(t_obs)
  v = viterbi(t_obs,hmm)
  display_sequence(v)