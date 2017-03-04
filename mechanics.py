#!/usr/bin/env python3

from read import read
from copy import deepcopy

#find the position of player in state matrix
def plyr_pos(state):
    for j in range(len(state)):                 #iterate rows
        for k in range(len(state[0])):          #iterate columns
            if state[j][k] == 2:                #if plyr found return indicies
                return j, k

#check if player is allowed to move to the left
def can_left(state, j, k):
    if k == 0:                                  #if at boundary
        return False
    if state[j][k-1] == 0:                      #if blank space ahead
        return True
    if state[j][k-1] == 1 and state[j][k-2] == 0:   #if blank space follows box
        return True
    return False                                #all other cases

#check if player is allowed to move to the right
def can_right(state, j, k):
    if k == len(state[0])-1:                    #if at boundary
        return False
    if state[j][k+1] == 0:                      #if blank space ahead
        return True
    if state[j][k+1] == 1 and state[j][k+2] == 0:   #if blank space follows box
        return True
    return False                                #all other cases

#check if player is allowed to move up
def can_up(state, j, k):
    if j == 0:                                  #if at boundary
        return False
    if state[j-1][k] == 0:                      #if blank space ahead
        return True
    if state[j-1][k] == 1 and state[j-2][k] == 0:   #if blank space follows box
        return True
    return False                                #all other cases

#check if player is allowed to move down
def can_down(state, j, k):
    if j == len(state)-1:                       #if at boundary
        return False
    if state[j+1][k] == 0:                      #if blank space ahead
        return True
    if state[j+1][k] == 1 and state[j+2][k] == 0:   #if blank space follows box
        return True
    return False                                #all other cases

#move to the left and return matrix
def mv_left(state, j, k):
    if state[j][k-1] == 1:          #if box ahead, push box in blank position
        state[j][k-1], state[j][k-2] = state[j][k-2], state[j][k-1]
    state[j][k], state[j][k-1] = state[j][k-1], state[j][k]    #move player fwd
    return state

#move to the right and return matrix
def mv_right(state, j, k):
    if state[j][k+1] == 1:          #if box ahead, push box in blank position
        state[j][k+1], state[j][k+2] = state[j][k+2], state[j][k+1]
    state[j][k], state[j][k+1] = state[j][k+1], state[j][k]    #move player fwd
    return state

#move up and return matrix
def mv_up(state, j, k):
    if state[j-1][k] == 1:          #if box ahead, push box in blank position
        state[j-1][k], state[j-2][k] = state[j-2][k], state[j-1][k]
    state[j][k], state[j-1][k] = state[j-1][k], state[j][k]    #move player fwd
    return state

#move down and return matrix
def mv_down(state, j, k):
    if state[j+1][k] == 1:          #if box ahead, push box in blank position
        state[j+1][k], state[j+2][k] = state[j+2][k], state[j+1][k]
    state[j][k], state[j+1][k] = state[j+1][k], state[j][k]    #move player fwd
    return state

#takes in current state and returns the list of valid neighbors
def neighbors(state):
    j, k = plyr_pos(state)
    neighbors_l = []
    if can_left(state, j, k):                   #if allowd to move left
        print("left")
        temp = deepcopy(state)
        neighbors_l.append(mv_left(temp, j, k))
    if can_right(state, j, k):                #if allowd to move right
        print("right")
        temp = deepcopy(state)
        neighbors_l.append(mv_right(temp, j, k))
    if can_up(state, j, k):                   #if allowed to move up
        print("up")
        temp = deepcopy(state)
        neighbors_l.append(mv_up(temp, j, k))
    if can_down(state, j, k):                 #if allowed tdo move down
        print("down")
        temp = deepcopy(state)
        neighbors_l.append(mv_down(temp, j, k))
    return neighbors_l


def main():
    test, _ = read()

    for row in test:
        print(row)

    neighbs = neighbors(test)
    for mtx in neighbs:
        for row in mtx:
            print(row)
        print()

if __name__ == "__main__":
    main()
