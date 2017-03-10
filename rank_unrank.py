#!/usr/bin/env python3

from read import read
import time

'''
>>Matrix to permuation<<
Input: State matrix
Output: Multiset permutation excluding walls
'''
def to_perm(state):
    multiset = []
    for j in range(len(state)):
        for k in range(len(state[0])):
            if state[j][k] == 3:
                continue
            multiset.append(state[j][k])
    return multiset

'''
>>Multiset permutation to state matrix<<
Input: Multiset permutation, walls matrix
Output: State matrix
'''
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
'''
>>Factorial<<
Input: Non-negative integer
Output: Factorial of input
'''
def fact(n):
    if n==0:                                    #base case
        return 1
    return n * fact(n-1)                        #recursive call

'''
>>Count the repetitions of each type<<
Input: Multiset permutation (sorted)
Output: List of number of repetitions for each type
'''
def counts(multiset):
    temp_set = multiset[:]                      #deep copy the multiset
    temp_set.sort()                             #sort the multiset
    ls = []
    for idx, u in enumerate(temp_set):          #for each number in multiset
        if u not in temp_set[:idx]:             #if not seen previously
            ls.append(1)                        #add one to count list
        else:                                   #if seen previously
            ls[-1] += 1                         #increment last value
    return ls

'''
>>Multinomial Coefficient<<
Input: Length of a multiset permutation, and the list of counts
Output: Multinomial Coefficient
'''
def multinom_coeff(n, ls):
    i = 1
    for v in ls:
        i *= fact(v)
    return int(fact(n) / i)


'''
>> Unrank for multiset permutation
Input: index, maximum potential, length, counts list
Output: corresponding multiset permutation
Index is the rank in lexicographic order, maximum potential is the total
number of possible permutations for given multiset, counts list is the list of
number of repetitions for each type of the multiset
NOTE: This unranking only works for consecutive multisets that start at 0
Source: http://zamboch.blogspot.com/2007/10/ranking-permutations-of-multiset-more.html
'''
def unrank(index, max_pot, length, counts_ls):
    result = [0 for x in range(length)]     #initialize list to store result
    curr_pot = max_pot                      #set potential to total permut #
    curr_len = length                       #set curr length to length of perm
    curr_counts = counts_ls[:]              #set curr counts to counts of types

    for i in range(curr_len):               #for each position of result list
        select = (index * curr_len) / curr_pot  #compute the selector
        offset, typ = 0, 0                      #initiliaze offset and type

        while (offset + curr_counts[typ]) <= select:    #scan for offset
            offset += curr_counts[typ]
            typ += 1

        index -= (curr_pot * offset) / curr_len         #subtract used offset
        curr_pot = (curr_pot * curr_counts[typ]) / curr_len #compute next potent
        curr_counts[typ] -= 1               #subtract one count of used type
        curr_len -= 1                       #update to length of sub-multiset
        result[i] = typ                     #store chosen type in result
    return result

'''
>>Rank multiset permutation<<
Input: multiset permutation, maximum potential, length, counts list
Output: index (rank)
Multiset permutation is the current permutation of the multiset, maximum
potential is the total number of permutations for the multiset, length is the
lenth of the multiset, counts list is the list of number of reptetitions for
each type of the multiset
NOTE: This ranking only works for consecutive multisets that start at 0
Source: http://zamboch.blogspot.com/2007/10/ranking-permutations-of-multiset-more.html
'''
def rank(multiset, max_pot, length, counts_ls):
    result = 0                              #initialize variable for result
    curr_pot = max_pot                      #set potential to total # of permut
    curr_len = length                       #set length to length of perm
    curr_counts = counts_ls[:]              #set curr counts to counts of types

    for i in range(curr_len):                   #for each position in given perm
        offset = 0                              #initiliaze offset
        typ = multiset[i]                       #set type to current pos of perm

        for u in range(typ):                    #compute sum of pot for subset
            offset += curr_counts[u]

        result += (curr_pot * offset) / curr_len    #add offset to rank/result
        curr_pot *= curr_counts[typ]            #compute pot of sub-multiset
        curr_pot /= curr_len
        curr_counts[typ] -= 1                   #subtract used type
        curr_len -= 1                           #update to length of sub-mutl
    return int(result)


'''
>>Ranking by Knuth<<
Input: Multiset permutation
Output: Index in lexicographic order
NOTE: This ranking works does work also for non-consecutive multisets that can
start with any number. However it is slower than Savara's algorithm, which does
the job for Sokoban.
Source: From Knuth - TAOCP, answer to question 7.2.1.2-4 (page 703)
'''

def rank_knuth(multiset):
    if len(multiset) == 1:
        return 0

    temp_set = multiset[:]                      #deep copy the multiset
    temp_set.sort()                             #sort the multiset
    n = len(multiset)

    #counts the num of elements to right of first element and smaller than it
    c = 0
    for x in range(1, len(multiset)):
        if multiset[x] < multiset[0]:
            c += 1

    count = counts(temp_set)
    coeff = multinom_coeff(n, count)

    result = c/n * coeff
    return int(result + rank_knuth(multiset[1:]))

'''
>>Information about one multiset<<
Input: multiset
Output: Maximum potential, length, counts list
Maximum potential is the total number of permutations for given multiset, length
is the length of the multiset, and counts list is the number a list of the
number of repetitions of each type in the multiset
This function is used to get information for the parameters of both the ranking
and unranking functions by Savara (not-Knuth) in this file
'''
def get_info(multiset):
    length = len(multiset)
    count = counts(multiset)
    max_pot = multinom_coeff(length, count)
    return max_pot, length, count

def main():
    start_time = time.time()

    test, _, walls, _, _ = read()
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
