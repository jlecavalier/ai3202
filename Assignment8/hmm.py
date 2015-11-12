class Hmm:
  def __init__(self,data,obs):
  	self.cond_probs = {}
  	self.tran_probs = {}
  	self.init_probs = {}

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