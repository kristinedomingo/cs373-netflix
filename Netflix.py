#!/usr/bin/env python3

# ---------------------------
# projects/netlifx/Netflix.py
# Copyright (C) 2015
# Xavier Micah Ramirez
# Kristine Domingo
# ---------------------------

# -------
# imports
# -------

import os
import pickle
import requests
import math
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
    movie_order a list of integers that are movie_ids
    return a dictionary {movie_id: [customer_ids]}
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
    return a dictionary {movie_id: {customer_id: rating}}
    """

    # Read a cache of movie rating averages
    if os.path.isfile(FILESYS_CACHE + 'kh549-movie_average.pickle'):
        # Read cache from file system
        with open(FILESYS_CACHE + 'kh549-movie_average.pickle', 'rb') as f:
            movie_avg_cache = pickle.load(f)
    else:
        # Read cache from HTTP
        bytes = requests.get(HTTP_CACHE + 'kh549-movie_average.pickle').content
        movie_avg_cache = pickle.loads(bytes)

    # Read a cache of the average ratings customers gave across all movies
    if os.path.isfile(FILESYS_CACHE + 'kh549-customer_average.pickle'):
        # Read cache from file system
        with open(FILESYS_CACHE + 'kh549-customer_average.pickle', 'rb') as f:
            cust_avg_cache = pickle.load(f)
    else:
        # Read cache from HTTP
        bytes = requests.get(HTTP_CACHE + 'kh549-customer_average.pickle').content
        cust_avg_cache = pickle.loads(bytes)

    # Read a cache of the years each movie was released
    if os.path.isfile(FILESYS_CACHE + 'pas2465-movie_years.pickle'):
        with open(FILESYS_CACHE + 'pas2465-movie_years.pickle', 'rb') as f:
            movie_years = pickle.load(f)
    else:
        # Read cache from HTTP
        bytes = requests.get(HTTP_CACHE + 'pas2465-movie_years.pickle').content
        movie_years = pickle.loads(bytes)

    # Read a cache of the avg ratings customers gave per decade
    if os.path.isfile(FILESYS_CACHE + 'mdg7227-avg_customer_rating_per_movie_decade.pickle'):
        with open(FILESYS_CACHE + 'mdg7227-avg_customer_rating_per_movie_decade.pickle', 'rb') as f:
            rating_per_decade = pickle.load(f)
    else:
        # Read cache from HTTP
        bytes = requests.get(HTTP_CACHE + 'mdg7227-avg_customer_rating_per_movie_decade.pickle').content
        rating_per_decade = pickle.loads(bytes)

    predictions_dict = {}

    # For each k, v in input_dict, fill predictions_dict with rating predictions
    # Format: {movie_id: [rating, rating, rating]}
    for movie_id, customer_id_list in input_dict.items():

        # Create an empty dictionary at movie_id
        predictions_dict[movie_id] = {}

        # Iterate through all customers for this movie
        for customer_id in customer_id_list:
            # "Baseline" number from article, the mean of all ratings
            baseline = 3.7

            # Get the "customer offset", based on the customer's average rating
            # for this movie's decade, or his average rating over all movies
            # (depending upon whether or not movie decade was available)
            if movie_years[movie_id] is not None:
                movie_decade = movie_years[movie_id] // 10 * 10
                cust_offset = rating_per_decade[customer_id][movie_decade]
            else:
                cust_offset = cust_avg_cache[customer_id]

            # Calculate the prediction: baseline + movie offset + cust offset
            predictions_dict[movie_id][customer_id] = baseline + (movie_avg_cache[movie_id] - baseline) + (cust_offset - baseline)

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
    return a float (root mean squared error)
    """

    rmse = 0.0
    sum = 0
    num_ratings = 0

    # Calculate RMSE
    for movie_id in predictions_dict:
        for customer_id in predictions_dict[movie_id]:
            num_ratings += 1
            cache_rating = cache[movie_id][customer_id]
            prediction = predictions_dict[movie_id][customer_id]
            sum += (cache_rating - prediction) ** 2

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
    movie_order a list of integers that are movie_ids
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

    if os.path.isfile(FILESYS_CACHE + 'mdg7227-real_scores.pickle'):
        # Read cache from file system
        with open(FILESYS_CACHE + 'mdg7227-real_scores.pickle', 'rb') as f:
            cache = pickle.load(f)
    else:
        # Read cache from HTTP
        bytes = requests.get(HTTP_CACHE + 'mdg7227-real_scores.pickle').content
        cache = pickle.loads(bytes)

    # Print RMSE
    w.write("RMSE: " + str(netflix_get_rmse(cache, predictions_dict))[:4])