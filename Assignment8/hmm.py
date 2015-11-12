class Hmm:
  def __init__(self,data,obs):
  	print("\nInitializing Hidden Markov Model. This may take a bit...")
  	print("\nGenerating emission probabilities...")
  	self.emis_probs = generate_emis_probs(data,obs)
  	print("Done!\n\nGenerating transition probabilities...")
  	self.tran_probs = generate_tran_probs(data)
  	print("Done!\n\nGenerating initial probabilities...")
  	self.init_probs = []
  	print("Done!\n")
  	self.verify_probs()
  
  def verify_probs(self):
    print("Checking whether all probabilities are distributed normally...")
    for i in range(26):
      e_prob = 0.0
      t_prob = 0.0
      for j in range(26):
        e_prob += self.emis_probs[i+(j*26)][1]
        t_prob += self.tran_probs[i+(j*26)][1]
      assert (abs(1-e_prob) <= 0.000000000000001)
      assert (abs(1-t_prob) <= 0.000000000000001)
    print("Everything okay!\n")

  def display_table(self):
    print("|\tS1\t|\tS2\t|\tP(S2|S1) (Emission Probability)\t|\tP(S2|S1)Transition Probability")
    for i in range(26):
      for j in range(26):
        o = self.emis_probs[(j*26)+i][0][0]
        s = self.emis_probs[(j*26)+i][0][1]
        pe = self.emis_probs[(j*26)+i][1]
        pt = self.tran_probs[(j*26)+i][1]
        print("|\t%s\t|\t%s\t|\t%.5f\t \t \t \t \t \t \t|\t%.5f" % (s,o,pe,pt))

def generate_emis_probs(data,obs):
  emis_probs = []
  for i in range(97,123):
    for j in range(97,123):
      p = single_emis_prob(chr(i),chr(j),data,obs)
      emis_probs.append([(chr(i),chr(j)),p])
  return emis_probs

def single_emis_prob(o,s,data,obs):
  s_count = 0
  o_count = 0
  for i in range(len(data)):
  	if data[i] == s:
  	  s_count += 1
  	  if obs[i] == o:
  	  	o_count += 1
  (num,den) = laplace_smoothing(o_count,s_count)
  return float(num) / float(den)

def generate_tran_probs(data):
  tran_probs = []
  for i in range(97,123):
    for j in range(97,123):
      p = single_tran_prob(chr(i),chr(j),data)
      tran_probs.append([(chr(i),chr(j)),p])
  return tran_probs

def single_tran_prob(s_now,s_prev,data):
  prev_count = 0
  now_count = 0
  for i in range(len(data)-1):
    if data[i] == s_prev:
      prev_count += 1
      if data[i+1] == s_now:
        now_count += 1
  (num,den) = laplace_smoothing(now_count,prev_count)
  return float(num) / float(den)

def laplace_smoothing(num_out,num_pos):
  return (num_out+1,num_pos+26)

def get_data_and_obs(f):
  data = []
  obs = []
  for line in f:
  	if line[0] != "_":
  	  data.append(line[0])
  	  obs.append(line[2])
  return (data,obs)

if __name__ == "__main__":
  (data,obs) = get_data_and_obs(open("typos20.data"))
  assert len(data) == len(obs)
  hmm = Hmm(data,obs)
  hmm.display_table()