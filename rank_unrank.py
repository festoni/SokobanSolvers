#!/usr/bin/env python3

from read import read
import time

#takes in the state matrix and returns a multiset permutation excluding walls
def to_perm(state):
    multiset = []
    for j in range(len(state)):
        for k in range(len(state[0])):
            if state[j][k] == 3:
                continue
            multiset.append(state[j][k])
    return multiset

#takes in a multiset permutation and boolean walls matrix, and returns the
#state matrix
def to_matrix(multiset, walls):
    #initialize matrix to all 0s
    matrix = [[0 for i in range(len(walls[0]))] for u in range(len(walls))]

    #run through walls matrix, and for all True entries, set matrix entries to 3
    for j in range(len(walls)):
        for k in range(len(walls[0])):
            if walls[j][k] == True:             #if you run into wall, set to 3
                matrix[j][k] = 3

    #run through entries of matrix, for every non 3 val, pop the first value in
    #the multiset and set it to current matrix entry. Note: this is mutable to
    #multiset list, so we initially make a deepcopy of it
    temp_set = multiset[:]                      #deepcopy the multiset
    for j in range(len(matrix)):
        for k in range(len(matrix[0])):
            if matrix[j][k] == 3:
                continue
            matrix[j][k] = temp_set.pop(0)      #equal to first value of set,pop

    return matrix


def main():
    start_time = time.time()

    test, _, walls = read()
    for row in test:
        print(row)
    sett = to_perm(test)
    print(sett)

    matrixx = to_matrix(sett, walls)
    for row in matrixx:
        print(row)

    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    main()
