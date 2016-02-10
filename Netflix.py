"""
Notes:
    - simplest possible solution: guess single number every time, 3.7
        - *** RESULTS IN RMSE OF 1.05 ***
    - fancier: mean + movie offset + user offset
        - example: Shawshank Redemption: 3.7 + 0.8 (movie offset) - 0.3 (user offset)
        - *** RESULTS IN RMSE OF 0.97 ***
    - since the input is always going to be in the format of probe.txt,
      netflix_read() should always read that input
        - we'll read cache files in another function, just not netflix_read()
"""

#!/usr/bin/env python3

# ---------------------------
# projects/collatz/Collatz.py
# Copyright (C) 2015
# Glenn P. Downing
# Xavier Micah Ramirez
# ---------------------------

# ------------
# netflix_read
# ------------

def netflix_read (stdin) :
    """
    stdin the inputstream
    return a dictionary of movie ids to lists of customer ids
    """
    movie_to_customer_db = {}

    for line in stdin:
        # If line is a movie id, add this key to the dictionary, splicing
        # off the colon and newline chararcter at the end
        if line.endswith(":\n"):
            current_movie = int(line[:len(line) - 2])
            movie_to_customer_db[current_movie] = []

        # Else, add the customer id to the associated movie
        else:
            movie_to_customer_db[current_movie].append(int(line))

    return movie_to_customer_db

# ------------
# netflix_eval
# ------------

def netflix_eval (i, j) :
    """
    i the beginning of the range, inclusive
    j the end       of the range, inclusive
    return the max cycle length of the range [i, j]
    """

    return max_so_far

# -------------
# netflix_print
# -------------

def netflix_print (w, i, j, v) :
    """
    print three ints
    w a writer
    i the beginning of the range, inclusive
    j the end       of the range, inclusive
    v the max cycle length
    """
    w.write(str(i) + " " + str(j) + " " + str(v) + "\n")

# -------------
# netflix_solve
# -------------

def netflix_solve (r, w) :
    """
    r a reader
    w a writer
    """
    big_dictionary = netflix_read(r) # reads entire file

    # for k, v in big_dictionary:

    # for s in r :
    #     if s != "":
    #         i, j = netflix_read(s)
    #         v    = netflix_eval(i, j)
    #         netflix_print(w, i, j, v)