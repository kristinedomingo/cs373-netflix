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

# -------
# imports
# -------

import os
import pickle
from numpy import mean, sqrt, square, subtract
from math import sqrt

# ------------
# netflix_read
# ------------

def netflix_read(stdin):
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

def netflix_eval(input_dict):
    """
    TODO
    """

    predictions_dict = {}

    # For each k, v in input_dict, fill predictions_dict with rating predictions
    # Format: {movie_id: [rating, rating, rating]}
    for movie_id, customer_id_list in input_dict.items():
        predictions_dict[movie_id] = {}
        for customer_id in customer_id_list:
            predictions_dict[movie_id][customer_id] = 3.7

    return predictions_dict

# ----------------
# netflix_get_rmse
# ----------------
def netflix_get_rmse(predictions_dict):
    rmse = 0.0

    if os.path.isfile('/u/fares/public_html/netflix-tests/mdg7227-real_scores.pickle') :
        # Read cache from file system
        f = open('/u/fares/public_html/netflix-tests/mdg7227-real_scores.pickle','rb')
        cache = pickle.load(f)

    sum = 0
    num_ratings = 0

    # Calculate RMSE
    for movie_id in predictions_dict:
        for customer_id in cache[movie_id]:
            num_ratings += 1
            sum += (cache[movie_id][customer_id] - predictions_dict[movie_id][customer_id]) ** 2

    return sqrt(sum / num_ratings)
# -------------
# netflix_print
# -------------

def netflix_print(w, predictions_dict):
    """
    TODO
    """

    # Write to standard output each movie id followed by predictions
    for movie_id, customer_id_list in predictions_dict.items():
        w.write(str(movie_id) + ":\n")

        # Converts every customer_id in the list to a string, and joins each
        # to a newline character
        w.write(('\n').join(map(str, customer_id_list)) + '\n')

    # Print RMSE
    print("RMSE: " + str(netflix_get_rmse(predictions_dict)))

# -------------
# netflix_solve
# -------------

def netflix_solve(r, w):
    """
    r a reader
    w a writer
    """

    # Read entire input file
    # {movie_id: [customer_id, customer_id, customer_id]}
    input_dict = netflix_read(r)

    # {movie_id: [rating, rating, rating]}
    predictions_dict = netflix_eval(input_dict)

    # Output to RunNetflix.out
    netflix_print(w, predictions_dict)