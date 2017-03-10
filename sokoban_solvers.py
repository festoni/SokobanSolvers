#!/usr/bin/env python3

from time import time
from heapq import heappop, heappush
from read import read
from rank_unrank import rank, unrank, to_perm, to_matrix, get_info
from mechanics import neighbors, is_goal
from heuristics import boxes, manhattan
from refinements import is_stuck
from math import inf
from astar_stuck import Astar_stuck, Astar_stuck2
from astar import a_star, a_star2
from best_fs import best_fs, best_fs2
from b_bound import b_bound, b_bound2
import fileinput

def main():

    start, goals, walls, goals_ls, boxes_ls = read()

    ##
    ##Comment out any of the function you don't want to use. For levels 10
    ##and higher, only use the rank/unrank implementiation of each search,
    ##(the name is followed by a 2 if ranking/unranking is used)
    ##

    print("\nBestFS")
    #BestFS no rank/unrank: heuristic can be: boxes, manhattan
    best_fs(start, goals, walls, boxes, cornered=True, verbose=False)
    #BestFS with rank/unrank: heuristic can be: boxes, manhattan
    best_fs2(start, goals, walls, boxes, cornered=True, verbose=False)

    print("\nA*")
    #A Star no rank/unrank: heuristic can be: boxes, manhattan
    a_star(start, goals, walls, boxes, cornered=True, verbose=False)
    #A Star with rank/unrank: heuristic can be: boxes, manhattan
    a_star(start, goals, walls, boxes, cornered=True, verbose=False)

    print("\nA* with is_stuck")
    #A Star using is_stuck: heuristic can be: boxes, manhattan
    Astar_stuck(start, goals, walls, boxes, boxes_ls, goals_ls, verbose=False)
    #A Star using is_stuck and rank/unrank: heuristic can be: boxes, manhattan
    Astar_stuck2(start, goals, walls, boxes, boxes_ls, goals_ls, verbose=False)

    print("\nBranch and Bound")
    #Branch and Bound no rank/unrank: heuristic can be: boxes, manhattan
    b_bound(start, goals, walls, boxes, cornered=True, verbose=False)
    #Branch and Bound with rank(no pruning): heuristic can be: boxes, manhattan
    b_bound2(start, goals, walls, boxes, cornered=True, verbose=False)


if __name__ == "__main__":
    main()
