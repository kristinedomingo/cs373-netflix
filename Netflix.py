#!/usr/bin/env python3

# ---------------------------
# projects/netlifx/Netflix.py
# Copyright (C) 2015
# Glenn P. Downing
# Xavier Micah Ramirez
# Kristine Domingo
# ---------------------------

# -------
# imports
# -------

import os
import pickle
import requests
from math import sqrt

FILESYS_CACHE = '/u/downing/public_html/netflix-caches/'
HTTP_CACHE = 'http://www.cs.utexas.edu/users/downing/netflix-caches/'

# ------------
# netflix_read
# ------------

def netflix_read(stdin, movie_order):
    """
    Reads movie ids and associated customer ids from standard input, and returns
    a dictionary of movie ids to lists of customer ids.
    stdin the inputstream
    """
    movie_to_customer_db = {}

    for line in stdin:
        # If line is a movie id, add this key to the dictionary, splicing
        # off the colon and newline chararcter at the end
        if line.endswith(":\n"):
            current_movie = int(line[:len(line) - 2])
            movie_order.append(current_movie)
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
    Obtains caches used to create predictions of customer ratings, and returns
    a dictionary of those predictions.
    input_dict a dict of input {movie_id: [customer_ids]}
    """

    if os.path.isfile(FILESYS_CACHE + 'kh549-movie_average.pickle') :
        # Read cache from file system
        f = open(FILESYS_CACHE + 'kh549-movie_average.pickle','rb')
        movie_avg_cache = pickle.load(f)
    else:
        # Read cache from HTTP
        bytes = requests.get(HTTP_CACHE + 'kh549-movie_average.pickle').content
        movie_avg_cache = pickle.loads(bytes)

    if os.path.isfile(FILESYS_CACHE + 'kh549-customer_average.pickle') :
        # Read cache from file system
        f = open(FILESYS_CACHE + 'kh549-customer_average.pickle','rb')
        cust_avg_cache = pickle.load(f)
    else:
        # Read cache from HTTP
        bytes = requests.get(HTTP_CACHE + 'kh549-customer_average.pickle').content
        cust_avg_cache = pickle.loads(bytes)

    predictions_dict = {}

    # For each k, v in input_dict, fill predictions_dict with rating predictions
    # Format: {movie_id: [rating, rating, rating]}
    for movie_id, customer_id_list in input_dict.items():
        predictions_dict[movie_id] = {}
        for customer_id in customer_id_list:
            predictions_dict[movie_id][customer_id] = 3.7 + (movie_avg_cache[movie_id] - 3.7) + (cust_avg_cache[customer_id] - 3.7)

    return predictions_dict

# ----------------
# netflix_get_rmse
# ----------------

def netflix_get_rmse(cache, predictions_dict):
    """
    Returns the root mean squared error (RMSE) of a dictionary of predictions,
    versus the actual ratings.
    cache a dictionary of the same format as predictions_dict, w/ actual ratings
    predictions_dict a dict of predictions {movie_id: {customer_id: rating}}
    """

    rmse = 0.0
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

def netflix_print(w, predictions_dict, movie_order):
    """
    Writes to writer w the contents of predictions_dict, movie ids followed by
    predicted customer ratings.
    w a writer
    predictions_dict a dict of predictions {movie_id: {customer_id: rating}}
    """

    # Write to standard output each movie id
    for movie_id in movie_order:
        w.write(str(movie_id) + ":\n")
        # Steps into a movie's dict of customer_id -> predicted_ratings and
        # writes the prediction to stdout
        for customer_id, prediction in predictions_dict[movie_id].items():
            # Converts every customer_id in the list to a string, and joins each
            # to a newline character
            w.write("%.2f\n" % prediction)

# -------------
# netflix_solve
# -------------

def netflix_solve(r, w):
    """
    Reads from reader r and initiates computation to generate Netflix
    rating predictions, and writes results to writer w. 
    r a reader
    w a writer
    """

    # Read entire input file
    # {movie_id: [customer_id, customer_id, customer_id]}
    movie_order = []
    input_dict = netflix_read(r, movie_order)

    # {movie_id: [rating, rating, rating]}
    predictions_dict = netflix_eval(input_dict)

    # Output to RunNetflix.out
    netflix_print(w, predictions_dict, movie_order)

    if os.path.isfile(FILESYS_CACHE + 'mdg7227-real_scores.pickle') :
        # Read cache from file system
        f = open(FILESYS_CACHE + 'mdg7227-real_scores.pickle','rb')
        cache = pickle.load(f)
    else:
        # Read cache from HTTP
        bytes = requests.get(HTTP_CACHE + 'mdg7227-real_scores.pickle').content
        cache = pickle.loads(bytes)

    # Print RMSE
    w.write("RMSE: %.2f" % netflix_get_rmse(cache, predictions_dict))
