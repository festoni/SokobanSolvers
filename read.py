#!/usr/bin/env python3
import fileinput, time

'''
Input: original input, length of longest line in input
Output: truncated input
Truncate input by removing the first column and the last overall column.
Also truncate the top most line and the bottom most line
'''
def preprocess(encoding, length):
    updated = ""
    for idx, line in enumerate(encoding.splitlines()):
        if idx == 0:                                #truncate first line
            continue
        if idx == len(encoding.splitlines())-1:     #truncate last line
            break
        if idx == len(encoding.splitlines())-2:     #don't add '\n' at last line
            updated += line[1:length-2]             #truncate ending '#\n'
        else:
            updated += line[1:length-2] + "\n"      #truncate '#\n' then add \n
    return updated


'''
Input: STDIN or Argument
Output: State matrix and Goals boolean matrix
Takes in input through STDIN or as argument, and gets rid of all the block not
in area of interest. Then it reads each character one by one, and sets the
corresponding entries in a state matrix. Goals are kept as spaces in state
matrix and are set as True in goals matrix.
'''
def read():
    # determine line of maximum length, such that we can truncate last columns
    length = 0
    encoding = ""
    for line in fileinput.input():
        encoding += line
        if len(line) > length:
            length = len(line)
    #if input was entered as stdin instead of argument, decrement desired length
    if '\r' in encoding:                            #takes care of added 'r'-s
        length -= 1

    #preprocess the input (remove blocks outside area of interest)
    proc_state = preprocess(encoding, length)

    #get the dimensions of the area of interest matrix
    rows = len(encoding.splitlines())-2             #num rows for state matrix
    cols = length - 3                               #num cols for state matrix

    #initialize state matrix to all 0s, and goals matrix to all False
    state = [[0 for i in range(cols)] for u in range(rows)]
    goals = [[False for i in range(cols)] for u in range(rows)]
    walls = [[False for i in range(cols)] for u in range(rows)]

    j, k = 0, 0                         #pointers to entries of states matricies
    for idx, ltr in enumerate(proc_state):
        if ltr == ' ':                  #floor
            k += 1                      #point to next column entry
        elif ltr == '\n':
            j += 1                      #set pointer to next row of matrix
            k = 0                       #set pointer to first column of matrix
        elif ltr == '#':                #walls
            state[j][k] = 3
            walls[j][k] = True
            k += 1
        elif ltr == '$':                #box
            state[j][k] = 1
            k += 1
        elif ltr == '*':                #box on goal
            state[j][k] = 1             #set state matrix entry to 1
            goals[j][k] = True          #set goals matrix entry to True
            k += 1
        elif ltr == '@':                #player
            state[j][k] = 2
            k += 1
        elif ltr == '+':                #player on goal
            state[j][k] = 2             #set state matrix entry to 2
            goals[j][k] = True          #set goals matrix entry to True
            k += 1
        elif ltr == '.':                #goal
            goals[j][k] = True
            k += 1

    return state, goals, walls


def main():
    start_time = time.time()

    state, goals, _ = read()

    #print state matrix and goal matrix
    for row in state:
        print(row)
    for row in goals:
        print(row)

    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    main()
