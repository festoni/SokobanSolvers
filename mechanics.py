#!/usr/bin/env python3

from read import read
from copy import deepcopy
import time

'''
>>Player position<<
Input: state matrix
Output: indicies to matrix entry where player is located
'''
def plyr_pos(state):
    for j in range(len(state)):                 #iterate rows
        for k in range(len(state[0])):          #iterate columns
            if state[j][k] == 2:                #if plyr found return indicies
                return j, k

'''
>>Is moving left allowed<<
Input: state matrix, player x index, player y index
Output: boolean
'''
def can_left(state, j, k):
    if k == 0:                                  #if at boundary
        return False
    if state[j][k-1] == 0:                      #if blank space ahead
        return True
    if k == 1:                                  #if wall follows box
        return False
    if state[j][k-1] == 1 and state[j][k-2] == 0:   #if blank space follows box
        return True
    return False                                #all other cases

'''
>>Is moving right allowed<<
Input: state matrix, player x index, player y index
Output: boolean
'''
def can_right(state, j, k):
    if k == len(state[0])-1:                    #if at boundary
        return False
    if state[j][k+1] == 0:                      #if blank space ahead
        return True
    if k == len(state[0])-2:                    #if wall follows box
        return False
    if state[j][k+1] == 1 and state[j][k+2] == 0:   #if blank space follows box
        return True
    return False                                #all other cases

'''
>>Is moving up allowed<<
Input: state matrix, player x index, player y index
Output: boolean
'''
def can_up(state, j, k):
    if j == 0:                                  #if at boundary
        return False
    if state[j-1][k] == 0:                      #if blank space ahead
        return True
    if j == 1:                                  #if wall follows box
        return False
    if state[j-1][k] == 1 and state[j-2][k] == 0:   #if blank space follows box
        return True
    return False                                #all other cases

'''
>>Is moving down allowed<<
Input: state matrix, player x index, player y index
Output: boolean
'''
def can_down(state, j, k):
    if j == len(state)-1:                       #if at boundary
        return False
    if state[j+1][k] == 0:                      #if blank space ahead
        return True
    if j == len(state)-2:                       #if wall follows space
        return False
    if state[j+1][k] == 1 and state[j+2][k] == 0:   #if blank space follows box
        return True
    return False                                #all other cases

'''
>>Move left<<
Input: state matrix, player x index, player y index, boolean whether to return
cost
Output: [cost], state after moving, change variable
The cost return value is in brackets because it is only returned if asked for,
The change variable is default to 9, but with be changed to 1 a box was moved
into leftmost column.
'''
def mv_left(state, j, k, with_cost=False):
    cost = 1
    change = 9
    if state[j][k-1] == 1:          #if box ahead, push box in blank position
        state[j][k-1], state[j][k-2] = state[j][k-2], state[j][k-1]
        if k == 2:                   #for is_stuck refinemnt, if into border
            change = 1
    state[j][k], state[j][k-1] = state[j][k-1], state[j][k]    #move player fwd
    if with_cost == False:
        return state, change
    else:
        return cost, state, change

'''
>>Move right<<
Input: state matrix, player x index, player y index, boolean whether to return
cost
Output: [cost], state after moving, change variable
The cost return value is in brackets because it is only returned if asked for,
The change variable is default to 9, but will be changed to 3 a box was moved
into rightmost column.
'''
def mv_right(state, j, k, with_cost=False):
    cost = 1
    change = 9
    if state[j][k+1] == 1:          #if box ahead, push box in blank position
        state[j][k+1], state[j][k+2] = state[j][k+2], state[j][k+1]
        if k == len(state[0])-2:        #for is_stuck refinemnt, if into border
            change = 3
    state[j][k], state[j][k+1] = state[j][k+1], state[j][k]    #move player fwd
    if with_cost == False:
        return state, change
    else:
        return cost, state, change

'''
>>Move up<<
Input: state matrix, player x index, player y index, boolean whether to return
cost
Output: [cost], state after moving, change variable
The cost return value is in brackets because it is only returned if asked for,
The change variable is default to 9, but will be changed to 0 a box was moved
into topmost row.
'''
def mv_up(state, j, k, with_cost=False):
    cost = 1
    change = 9
    if state[j-1][k] == 1:          #if box ahead, push box in blank position
        state[j-1][k], state[j-2][k] = state[j-2][k], state[j-1][k]
        if j == 2:                  #for is_stuck refinemnt, if into border
            change = 0
    state[j][k], state[j-1][k] = state[j-1][k], state[j][k]    #move player fwd
    if with_cost == False:
        return state, change
    else:
        return cost, state, change

'''
>>Move down<<
Input: state matrix, player x index, player y index, boolean whether to return
cost
Output: [cost], state after moving, change variable
The cost return value is in brackets because it is only returned if asked for,
The change variable is default to 9, but will be changed to 0 a box was moved
into bottom most row.
'''
def mv_down(state, j, k, with_cost=False):
    cost = 1
    change = 9
    if state[j+1][k] == 1:          #if box ahead, push box in blank position
        state[j+1][k], state[j+2][k] = state[j+2][k], state[j+1][k]
        if j == len(state)-3:           #for is_stuck refinemnt, if into border
            change = 2
    state[j][k], state[j+1][k] = state[j+1][k], state[j][k]    #move player fwd
    if with_cost == False:
        return state, change
    else:
        return cost, state, change

#takes in current state and returns the list of valid neighbors
'''
>>Neighbors of a state<<
Input: state, and boolean whether to return cost as well
Output: list of the neighbors of given state matrix [with cost]
'''
def neighbors(state, with_cost=False):
    j, k = plyr_pos(state)
    neighbors_l = []
    if can_left(state, j, k):                   #if allowd to move left
        temp = deepcopy(state)
        if with_cost == False:
            neighbors_l.append(mv_left(temp, j, k))
        else:
            neighbors_l.append(mv_left(temp, j, k, with_cost=True))
    if can_right(state, j, k):                #if allowd to move right
        temp = deepcopy(state)
        if with_cost == False:
            neighbors_l.append(mv_right(temp, j, k))
        else:
            neighbors_l.append(mv_right(temp, j, k, with_cost=True))
    if can_up(state, j, k):                   #if allowed to move up
        temp = deepcopy(state)
        if with_cost == False:
            neighbors_l.append(mv_up(temp, j, k))
        else:
            neighbors_l.append(mv_up(temp, j, k, with_cost=True))
    if can_down(state, j, k):                 #if allowed tdo move down
        temp = deepcopy(state)
        if with_cost == False:
            neighbors_l.append(mv_down(temp, j, k))
        else:
            neighbors_l.append(mv_down(temp, j, k, with_cost=True))
    return neighbors_l

'''
>>Goal check<<
Input: state matrix, goals matrix
Output: boolean if state matrix is a goal matrix
'''
def is_goal(state, goals):
    for j in range(len(state)):             #check all the matrix for boxes
        for k in range(len(state[0])):
            if state[j][k] == 1:            #for each location of a box
                if goals[j][k] == False:    #check the corresp goal location
                    return False            #return false if a box is unmatched
    return True                             #return true if all boxes matched


def main():
    start_time = time.time()
    test, _, _, _, _ = read()

    for row in test:
        print(row)
    print()

    neighbs = neighbors(test)
    for mtx,_ in neighbs:
        for row in mtx:
            print(row)
        print()

    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    main()
