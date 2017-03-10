#!/usr/bin/env python3
import fileinput, time

'''
>>Preprocess<<
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
>>Update list<<
Input: list of length 4, x index of matrix, y index of matrix, # rows, # cols
Output: updated list of length 4
This function takes in a list of length 4, where ls[0] corresponds to topmost
row, ls[1] to leftmost column, ls[2] to bottom most row, and ls[3] to
rightmost column. Is is only called when a box or goal is found is one of these
borders. And it will update the index of the list in which the indices are in.
Used only for the is_stuck refinement.
'''
def update_ls(ls, j, k, rows, cols):
    if j == 0:
        ls[0] += 1
    elif j == rows-1:
        ls[2] += 1
    if k == 0:
        ls[1] += 1
    elif k == cols-1:
        ls[3] += 1
    return ls

'''
>> Read <<
Input: STDIN or Argument
Output: State matrix, goals boolean matrix, walls boolean matrix, list of boxes
in borders, and list of goals in borders
Takes in input through STDIN or as argument, and gets rid of all the blocks not
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

    goals_ls = [0]*4       #[top row, left column, bottom row, right column]
    boxes_ls = [0]*4       #[top row, left column, bottom row, right column]

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
            temp = boxes_ls[:]
            boxes_ls = update_ls(temp, j, k, rows, cols)    #update boxes list
            k += 1
        elif ltr == '*':                #box on goal
            state[j][k] = 1             #set state matrix entry to 1
            goals[j][k] = True          #set goals matrix entry to True
            temp = goals_ls[:]
            goals_ls = update_ls(temp, j, k, rows, cols)    #update goals list
            temp = boxes_ls[:]
            boxes_ls = update_ls(temp, j, k, rows, cols)    #update boxes list
            k += 1
        elif ltr == '@':                #player
            state[j][k] = 2
            k += 1
        elif ltr == '+':                #player on goal
            state[j][k] = 2             #set state matrix entry to 2
            goals[j][k] = True          #set goals matrix entry to True
            temp = goals_ls[:]
            goals_ls = update_ls(temp, j, k, rows, cols)    #update goals list
            k += 1
        elif ltr == '.':                #goal
            goals[j][k] = True
            temp = goals_ls[:]
            goals_ls = update_ls(temp, j, k, rows, cols)    #update goals list
            k += 1

    return state, goals, walls, goals_ls, boxes_ls


def main():
    start_time = time.time()

    state, goals, _, _, _ = read()

    for row in state:
        print(row)
    for row in goals:
        print(row)

    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    main()
