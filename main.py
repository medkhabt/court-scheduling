import sys 
import math
import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt

# M is the set of matches edges.
def visualize(M):
    G = nx.Graph()
    G.add_nodes_from(M['X'], bipartite=0)
    print(f"the node set in X is {M['X']}")
    G.add_nodes_from(M['Y'], bipartite=1)
    print(f"the node set in Y is {M['Y']}")
    G.add_edges_from(M['edges'])
    print(f"the edge set is {M['edges']}")
    pos = dict()
    xlen = len(M['X'])
    ylen = len(M['Y'])
    pos.update( (n, (1, xlen - i)) for i, n in enumerate(M['X']) ) 
    pos.update( (n, (2, ylen - i)) for i, n in enumerate(M['Y']) ) 
    nx.draw_networkx(G, pos=pos)
    plt.show()
def cantorPairing(x,y):
    return int((x + y + 1)*(x + y) / 2) + y  
def inverseCantorPairing(z): 
    w = int(math.floor((math.sqrt(8*z + 1) - 1) / 2 ))
    t = int((w * w + w )/ 2)
    y = z - t
    return (w - y, y)
###
# I I set of edges.
# E: set of edges 
# e: edge e 
# n: teams
# p: rounds
def constraintGame(I,E,e,n,m,p):
    # taking the match vertex from the edge. 
    #print("********* In constraintGame")
    #breakpoint()
    I.append((e[0], e[1]))

    (Ti, Tj) = inverseCantorPairing(e[0])
    posCourt = (e[1]%m) 
    if(posCourt == 0):
        posCourt = m;
    roundPos = posCourt
    #print(f"the range of the loop is 0 to {m} with poscourt {posCourt}")
    for Tk in range(1, n+1): 
        #print("---- begin: direct -----")
        # Fix this part.
        for l in range(1, posCourt):
            timeRound = e[1] - l 
            #print(f"choice in Ti {Ti}:: check Tk = {Tk} weither ({Tk}, {timeRound}) exists in E and this for the selected edge {e[1]}")
            #print(f" TI 0 -> pos::check {Tk} in comparaison to ({Ti}, {Tj})  with e1: {e[1]} and l : {l} value for court-round {timeRound}")
            if(Tk != Ti and Tk != Tj): 
                if(timeRound == e[1]):
                    continue

                mx = cantorPairing(min([Ti,Tk]), max([Ti,Tk]))
                my = cantorPairing(min([Tj, Tk]), max([Tj, Tk]))
                for v, w in E: 
                    if(v == mx and w == timeRound):
                        #print(f"direct Ti => add the {Ti} ,{Tk} with {e[1] - (l-posCourt)} to the ignore list")
                        #breakpoint()
                        I.append((cantorPairing(min([Ti,Tk]), max([Ti,Tk])), timeRound))
                    if(v == my and w == timeRound):
                        #breakpoint()
                        I.append((cantorPairing(min([Tj, Tk]), max([Tj, Tk])), timeRound))
                        #print(f"direct Tj => add the {Tj, Tk} with {e[1] - (l-posCourt)} to the ignore list")
        #print("---- end direct")
        #print("---- begin reverse")
        for l in range(1, m - posCourt + 1):
            timeRound = e[1] + l 
            #print(f" TI 0 -> m-pos::check {Tk} in comparaison to ({Ti}, {Tj})  with e1: {e[1]} and l : {l} value for court-round {timeRound}")
            #print(f"And the ({Ti}, {Tk}) is {cantorPairing(Ti, Tk)}")
            #print(f" And edges are {E}")

            if(Tk != Ti and Tk != Tj): 
                if(timeRound == e[1]):
                    continue
                mx = cantorPairing(min([Ti,Tk]), max([Ti,Tk]))
                my = cantorPairing(min([Tj, Tk]), max([Tj, Tk]))
                for v, w in E: 
                    if(v == mx and w == timeRound):
                        #print(f"reverse: Ti => add the ({Ti} ,{Tk}) with {timeRound} to the ignore list")
                        #breakpoint()
                        I.append((cantorPairing(min([Ti,Tk]), max([Ti,Tk])), timeRound))
                    if(v == my and w == timeRound):
                        #breakpoint()
                        I.append((cantorPairing(min([Tj, Tk]), max([Tj, Tk])), timeRound))
                        #print(f"reverse: Tj => add the ({Tj}, {Tk}) with {timeRound} to the ignore list")
        #print("---- end reverse")
        ##print("---- start round constraint")
        #for i in range(roundPos, m*p, p):
        #    if(Tk != Ti and Tk != Tj): 
        #        mx = cantorPairing(min([Ti,Tk]), max([Ti,Tk]))
        #        my = cantorPairing(min([Tj, Tk]), max([Tj, Tk]))
        #        #breakpoint()
        #        I.append((cantorPairing(min([Ti,Tk]), max([Ti,Tk])), i))
        #        #breakpoint()
        #        I.append((cantorPairing(min([Tj, Tk]), max([Tj, Tk])), i))
        #print("---- end round constraint")
def getTeamsFromGame(game):
    (x,y) = inverseCantorPairing(game)
    return f"({x}, {y})"
def main():
    E = []
    M = []

# 1 ) define n teams 
    n = int(sys.argv[1])
    m = int(sys.argv[2])
    p = int(sys.argv[3])
    
    #print(n)
# 2 ) calculate the indices of the matches. 
# 3 ) define the number of courts and rounds 
# 4 ) generate vertices from 1 to m*p for the subset of court-roudns
    M_visual = {'X': [], 'Y' : [], 'edges': []}
    for i in range(1, n):
        for j in range(i + 1, n + 1):
            for k in range (1, m*p + 1):
                x = f"({i}, {j})"
                if(x not in M_visual['X']):
                    M_visual['X'].append(x)
                courtX = k%m 
                if (courtX == 0): 
                    courtX = m
                roundX = int((k - 1) / 2) + 1
                y=f"C{courtX}-R{roundX}"
                if(k not in M_visual['Y']):
                    M_visual['Y'].append(y)
                E.append((cantorPairing(i,j), k))
#    print("games")
#    for e in E: 
#        print(e[0])
# 5 ) do a matching algorithm.
    ignore = []
    for v,w in E:
        matching = True
        for vm, wm in M:
            if(v == vm or v == wm or w == vm or w == wm):
                matching = False
                break
        if(matching and (v,w) not in ignore):
            #print(f"the edge to add is ({v}, {w}) and the ignored edges are {ignore}")
            M.append((v,w))
            x = inverseCantorPairing(v)
            x = f"({x[0]}, {x[1]})"
            courtX = w%m 
            if (courtX == 0): 
                courtX = m
            roundX = int((w - 1) / 2) + 1
            y=f"C{courtX}-R{roundX}"
            M_visual['edges'].append((x, y))

            constraintGame(ignore, E, (v,w), n, m, p)
            # remove other matchs that have the same i or j. that are not this match.


    #print(f"(n={n}, m={m}, p={p})")
    for v,w in M:
        courtX = w%m 
        if (courtX == 0): 
            courtX = m
        roundX = int((w - 1) / 2) + 1
        print(f" {w} | Court {courtX} Round {roundX} We have the game: {getTeamsFromGame(v)}")
    #breakpoint()
    visualize(M_visual)
main()
