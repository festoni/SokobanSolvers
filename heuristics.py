#!/usr/bin/env python3

from read import read

#takes in state matrix and goal matrix, checks the location of the boxes in
#state matrix with corresponding location in goals matrix, only counts when
#corresponding value in goals matrix is False, returns the unmatched boxes count
def boxes(state, goals):
    boxes = []
    for j in range(len(state)):             #check all the matrix for boxes
        for k in range(len(state[0])):
            if state[j][k] == 1:            #record the locations of all boxes
                boxes.append((j, k))
    unmatch = 0
    for v in boxes:                         #check each box location if on goal
        if not goals[v[0]][v[1]]:           #if box not on goal, increment count
            unmatch += 1
    return unmatch                          #return number of unmatched goals

def manhattan(state, goals):
    boxes = []
    for j in range(len(state)):             #check all the matrix for boxes
        for k in range(len(state[0])):
            if state[j][k] == 1:            #record the locations of all boxes
                boxes.append((j, k))

    goals_l = []
    for j in range(len(goals)):             #check all the matrix for goals
        for k in range(len(goals[0])):
            if goals[j][k] == True:         #record the locations of all goals
                goals_l.append((j, k))

    tot_dist = 0
    for idx1 in boxes:                      #iterate through each box
        local_tot = 9999                    #set temporary distance very high
        for idx2 in goals_l:                #iterate through each goal for box
            dist_h = abs(idx1[0] - idx2[0]) #calc horiz dist of box and goal
            dist_v = abs(idx1[1] - idx2[1]) #calc vert dist of box and goal
            local_tot = min(dist_h + dist_v, local_tot) #take the minimum dist
        tot_dist += local_tot               #add the minimmum box-goal dist
    return tot_dist                         #return the total min manhattan dist


def main():
    test_m, test_g = read()

    print(boxes(test_m, test_g))
    print(manhattan(test_m,test_g))

if __name__ == "__main__":
    main()
