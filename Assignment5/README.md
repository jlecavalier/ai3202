# ai3202
Implementation of the iteration value algorithm for CSCI 3202

# The relationship between epsilon and the path discovered by iteration value
Different values of epsilon can produce different solutions to the problem. First, a brief explanation on how this can be:

At each iteration of this algorithm, the expected utility of each state is calculated. However, due to the probabilistic nature of the transition relation, the algorithm makes errors at each iteration. The value of epsilon is a factor in the maximum allowable error for any given state. The maximum allowable error is given by:

epsilon * (1 - discount_factor) / discount_factor

In our problem, the discount factor is .9 and the default value of epsilon is .5. This means that, by default, the maximum allowable error is about .06, which is pretty small. This is a good thing. This means that, given enough time, the algorithm will produce a policy for optimally navigating the maze such that the maximum error during any given state is less than or equal to about .06.

# Results for different epsilon values
Here are the results for epsilon = 0.5, 0.1, and 1:
Location: (7,0) Utility: 56.8596 Action: right
Location: (7,1) Utility: 64.3117 Action: right
Location: (7,2) Utility: 73.3828 Action: right
Location: (7,3) Utility: 83.6403 Action: right
Location: (7,4) Utility: 94.4160 Action: right
Location: (7,5) Utility: 107.0155 Action: right
Location: (7,6) Utility: 121.9443 Action: up
Location: (6,6) Utility: 139.8144 Action: up
Location: (5,6) Utility: 157.8971 Action: up
Location: (4,6) Utility: 177.7725 Action: up
Location: (3,6) Utility: 200.9728 Action: right
Location: (3,7) Utility: 231.8512 Action: up
Location: (2,7) Utility: 266.5892 Action: up
Location: (1,7) Utility: 299.4423 Action: up
Location: (0,7) Utility: 341.0970 Action: right
Location: (0,8) Utility: 395.1328 Action: right

The path for all three of these is the same. This is reasonable since, even when epsilon is 1, the maximum allowable error is about .1, which is still pretty small. However, when we increase epsilon to 100, we get different results:

Location: (7,0) Utility: 2.0324 Action: up
Location: (6,0) Utility: 2.6077 Action: up
Location: (5,0) Utility: 3.5097 Action: up
Location: (4,0) Utility: 5.1149 Action: right
Location: (4,1) Utility: 9.6982 Action: up
Location: (3,1) Utility: 18.3468 Action: up
Location: (2,1) Utility: 28.9452 Action: right
Location: (2,2) Utility: 45.2185 Action: right
Location: (2,3) Utility: 61.7959 Action: right
Location: (2,4) Utility: 80.4514 Action: up
Location: (1,4) Utility: 104.1796 Action: up
Location: (0,4) Utility: 131.0984 Action: right
Location: (0,5) Utility: 166.7362 Action: right
Location: (0,6) Utility: 207.1875 Action: right
Location: (0,7) Utility: 250.0615 Action: right
Location: (0,8) Utility: 304.0972 Action: right

This time, we see that the horse takes a slightly different path that isn't as good as the first one (this one goes over more mountains and snakes and goes through fewer barns). When we increase epsilon all the way to 450 or higher, the algorithm fails to come up with a policy that is likely to make it to the goal. When epsilon is 450, the program outputs the following results:

Location: (7,0) Utility: 0.0000 Action: up
Location: (6,0) Utility: 0.0000 Action: left
Policy unlikely to reach goal...

# Explanation of results
1) Why is the path the same when epsilon is between zero and one? This is because such values for epsilon give us a maximum allowable error of less than 1/10, which is small enough for the algorithm to find the optimal solution.

2) Why is the solution not optimal when epsilon is 100? This is because an epsilon value of 100 gives us a maximum allowable error of about 11.1, which is pretty high. This means that we allow the estimated utility of any state to be different from the actual utility by at most 11.1, so we are likely to see a few subtle errors here and there.

3) Why does the algorithm fail to produce a solution which is likely to reach the goal when epsilon is 450? This is due to the nature of the problem. Before the first iteration of the algorithm, the estimated utility of each state is set to zero. The actual utility of the goal state is 50, so the expected utility after the first iteration should be slightly less than 50. This is going to be the largest error made during the first iteration of the algorithm, and it is an error of about 50 utility. However, an epsilon value of 450 produces a maximum allowable error of exactly 50, which means that the algorithm only runs for a single iteration. The errors are going to be so massive that the policy produced by the algorithm will be rather unlikely to guide the horse to the goal.