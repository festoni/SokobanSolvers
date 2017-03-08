#!/usr/bin/env python3
from read import read

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


def main():
    test, goals, _ = read()
    print(test, goals)
    print(is_cornered(test, goals, 1,3))


if __name__ == "__main__":
    main()
