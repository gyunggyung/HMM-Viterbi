#!/usr/bin/env python

# Code from the wikipedia page for Viterbi algorithm done or modified by Zhubarb
# More implementations of Viterbi algorithm can be found at http://stackoverflow.com/questions/9729968/python-implementation-of-viterbi-algorithm
# Example of implementation of the viterbi algorithm for a  primitive clinic in a village.
# People in the village have a very nice property that they are either healthy or have a fever.
# They can only tell if they have a fever by asking a doctor in the clinic.
# The wise doctor makes a diagnosis of fever by asking patients how they feel.
# Villagers only answer that they feel normal, dizzy, or cold.

states = ('B', 'A')
 
observations = ('x', 'y', 'y')
 
start_probability = {'A': 0.7, 'B': 0.3}
 
transition_probability = {
    'A': {'A': 0.2, 'B': 0.7, '</s>': 0.1}, 
    'B': {'A': 0.7, 'B': 0.2, '</s>': 0.1}
    }

emission_probability = {
    'A': {'x': 0.4, 'y': 0.6}, 
    'B': {'x': 0.3, 'y': 0.7}
    }

# Helps visualize the steps of Viterbi.
def print_dptable(V):
    s = "    " + " ".join(("%7d" % i) for i in range(len(V))) + "\n"
    for y in V[0]:
        s += "%.5s: " % y
        s += " ".join("%.7s" % ("%f" % v[y]) for v in V)
        s += "\n"
    print(s)
    
def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]
    path = {}
 
    # Initialize base cases (t == 0)
    for y in states:
        print(y)
        V[0][y] = start_p[y] * emit_p[y][obs[0]]
        path[y] = [y]
        print(V)
        print(path)
 
    # alternative Python 2.7+ initialization syntax
    # V = [{y:(start_p[y] * emit_p[y][obs[0]]) for y in states}]
    # path = {y:[y] for y in states}
 
    # Run Viterbi for t > 0
    for t in range(1, len(obs)):
        V.append({})
        newpath = {}
 
        for y in states:
            (prob, state) = max((V[t-1][y0] * trans_p[y0][y] * emit_p[y][obs[t]], y0) for y0 in states)

            V[t][y] = prob
            #print("gggg", path[state] + [y])
            #print("eeee", path[state], [y])
            newpath[y] = path[state] + [y]
            print("d",newpath)
        # Don't need to remember the old paths
        path = newpath
 
    print_dptable(V)
    

    
    (prob, state) = max((V[t][y], y) for y in states)
    return (prob, path[state])

def example():
    return viterbi(observations,
                   states,
                   start_probability,
                   transition_probability,
                   emission_probability)
print(example())