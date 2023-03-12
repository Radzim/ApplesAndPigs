from numpy.random import choice

def make_move(row):
    s = row['successors']
    e = row['successors_evals']
    t = row['successors_trickiness']
    target = e[s.index(row['best_move'])]
    s = [s[i] for i in range(len(e)) if e[i] == target]
    t = [t[i]+1 for i in range(len(e)) if e[i] == target]
    return choice(s, 1, p=[tt/sum(t) for tt in t])[0]


