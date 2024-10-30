# Court Scheduling 
## Problem 
I usually play basketball and volleyball in the sportcenter of the uni passau. 
The number of present people vary and the court number varies, so we usally have problems 
when trying to choose which team plays where and when and keep it fair at the same time. 
## Intuition
I started working on some work related to graph theory. The problem looked to me close to a 
matching problem, where the games (Ti against Tj) is a subset from the vertex set in the graph 
and the pair of court and time is compose the vertices in the other subset of the graph. 

I also had to add some constraints after picking a matching edge, as for example if the team 1 
plays in the court 1 during the round 1, than it is not possible for it to play an other game 
in one of the other courts in the same round, and this is not described on the graph with the current 
setup, so i had to add the constraints while looking for new matches. 

## further work 
For now the graph is unweighted, and the algo is greedy, so the team 1 has the most number of games. 
A way to solve this is by adding weights and changing them dynamically, depending on the set of 
matching edges that we already have. 
