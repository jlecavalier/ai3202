class Hmm:
  def __init__(self,data,obs):
  	print("\nInitializing Hidden Markov Model. This may take a bit...\n")
  	print("\nGenerating emission probabilities...")
  	self.emis_probs = generate_emis_probs(data,obs)
  	print("Done!\n\nGenerating transition probabilities...")
  	self.tran_probs = []
  	print("Done!\n\nGenerating initial probabilities...")
  	self.init_probs = []
  	print("Done!\n\n")

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