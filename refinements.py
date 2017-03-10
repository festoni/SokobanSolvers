#!/usr/bin/env python3
from read import read

'''
>>Box in corner<<
Input: State matrix, goals matrix, x index of player, y index of player
Output: Boolean if box is in corner that is not goal
'''
def is_cornered(state, goals, j, k):
    if goals[j][k] == True:                     #if box on goal, return false
        return False

    if j-1 == -1 or state[j-1][k] == 3:         #if border or wall on top
        if k-1 == -1 or state[j][k-1] == 3:     #if border or wall on left
            return True
        if k+1 == len(state[0]) or state[j][k+1] == 3: #if border or wall right
            return True

    if j+1 == len(state) or state[j+1][k] == 3: #if border or wall on bottom
        if k-1 == -1 or state[j][k-1] == 3:     #if border or wall on left
            return True
        if k+1 == len(state[0]) or state[j][k+1] == 3: #if border or wall right
            return True
    return False

'''
>>Boxes stuck<<
Input: Goals in borders list, boxes in borders list, change variable
Output: boolean if boxes are stuck
This function takes in the following parameters where the change variable
specifies at which border was a boxed move into. Goals list and boxes list are
both length 4, where ls[0] is count for goals, boxes in topmost row
(respectively), ls[1] is count for leftmost column, ls[2] count for bottom most
row, and ls[3]. Each time one of these values of the box list is greater than
the corresponding value in the goals list, then it's a stuck state.
'''
def is_stuck(gl, bx, chng):
    if chng != 9:
        bx[chng] += 1
    for i in range(4):
        if gl[i] < bx[i]:
            return True, bx
    return False, bx

def main():
    test, goals, _, goals_ls, boxes = read()
    print(test, goals)
    print(is_cornered(test, goals, 1,3))



if __name__ == "__main__":
    main()
