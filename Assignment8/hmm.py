class Hmm:
  def __init__(self,data,obs):
    # First, we generate all the probabilities we need for the HMM
  	print("\nInitializing Hidden Markov Model. This may take a bit...")
  	print("\nGenerating emission probabilities...")
  	self.emis_probs = generate_emis_probs(data,obs)
  	print("Done!\n\nGenerating transition probabilities...")
  	self.tran_probs = generate_tran_probs(data)
  	print("Done!\n\nGenerating initial probabilities...")
  	self.init_probs = generate_init_probs(data)
  	print("Done!\n")

    # Afterwards, we verify that our results actually make up
    # a probabilistic distribution (i.e. each appropriate
    # set of probabilities sum to one)
  	self.verify_probs()
  
  # This function checks whether each of our probabilities are distributed
  # If we fix S2 and let S1 be an element of {a,b,c,d,...,z}, then
  # the big sum of P(S2|S1) should sum to exactly one.
  def verify_probs(self):
    print("Checking whether all probabilities are distributed properly...")
    i_prob = 0.0
    for i in range(26):
      e_prob = 0.0
      t_prob = 0.0
      i_prob += self.init_probs[i][1]
      for j in range(26):
        e_prob += self.emis_probs[i+(j*26)][1]
        t_prob += self.tran_probs[i+(j*26)][1]
      # Since there is floating point error in computing the probabilities,
      # we allow the distribution sums to differ from 1 by at most 10^(-15)
      assert (abs(1-e_prob) <= 0.000000000000001)
      assert (abs(1-t_prob) <= 0.000000000000001)
    assert (abs(1-i_prob) <= 0.000000000000001)
    print("Everything okay!\n")

  # This function displays all of our probabilities in a nice table.
  # The table doesn't look very nice in a terminal, so you should probably
  # pipe it to an output file...
  def display_table(self):
    print("Writing probabilities to a file...")
    f_emis = open('emission_probabilities.data', 'w+')
    f_emis.write("P(Et | Xt)\n\n")
    f_tran = open('transition_probabilities.data', 'w+')
    f_tran.write("P(Xt+1 | Xt)\n\n")
    f_init = open('initial_probabilities.data', 'w+')
    f_init.write("P(X)\n\n")
    for i in range(26):
      f_init.write("P(%s) = %.5f\n" % (self.init_probs[i][0],self.init_probs[i][1]))
      for j in range(26):
        o = self.emis_probs[(j*26)+i][0][0]
        s = self.emis_probs[(j*26)+i][0][1]
        pe = self.emis_probs[(j*26)+i][1]
        pt = self.tran_probs[(j*26)+i][1]
        f_emis.write("P(%s | %s) = %.5f\n" % (o,s,pe))
        f_tran.write("P(%s | %s) = %.5f\n" % (o,s,pt))
    print("Done!\n")

# Calculate the initial probability of each letter
def generate_init_probs(data):
  init_probs = []
  for i in range(97,123):
    l_count = 0
    for j in range(len(data)):
      if data[j] == chr(i):
        l_count += 1
    (num,den) = laplace_smoothing(l_count,len(data))
    p = float(num) / float(den)
    init_probs.append([chr(i),p])
  return init_probs

# Generates all the emission probabilities
def generate_emis_probs(data,obs):
  emis_probs = []
  for i in range(97,123):
    for j in range(97,123):
      p = single_emis_prob(chr(i),chr(j),data,obs)
      emis_probs.append([(chr(i),chr(j)),p])
  return emis_probs

# Given an observation and a state, generate
# the emission probability. i.e., generate
# the probability of observing o given that we
# are in state s.
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

# Generates all the transition probabilities
def generate_tran_probs(data):
  tran_probs = []
  for i in range(97,123):
    for j in range(97,123):
      p = single_tran_prob(chr(i),chr(j),data)
      tran_probs.append([(chr(i),chr(j)),p])
  return tran_probs

# Given two states, generate the transition probability.
# i.e., generate the probability of transitioning to 
# s_now, given that we are in s_prev.
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

# Smooths a probability using Laplace smoothing.
# We add 1 to the numerator and we add the number
# of possible outputs to the denominator. There
# are 26 lower case letters, so there are 26 possible
# outputs.
def laplace_smoothing(num_out,num_pos):
  return (num_out+1,num_pos+26)

# Converts the data file into two arrays. One
# contains the raw data, and the other contains
# our observations.
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