#!/usr/bin/env python3

# -------------------------------
# projects/collatz/TestCollatz.py
# Copyright (C) 2015
# Glenn P. Downing
# Xavier Micah Ramirez
# Kristine Domingo
# -------------------------------

# -------
# imports
# -------

from io       import StringIO
from unittest import main, TestCase

from Netflix import    \
     netflix_read,     \
     netflix_eval,     \
     netflix_get_rmse, \
     netflix_print,    \
     netflix_solve

# -----------
# TestNetflix
# -----------

class TestNetflix (TestCase) :
    def setUp(self):
        self.input1 = StringIO("1000:\n"
                                "2326571\n"
                                "977808\n"
                                "1010534\n"
                                "1861759\n"
                                "79755\n"
                                "98259\n"
                                "1960212\n"
                                "97460\n"
                                "2623506\n"
                                "2409123\n"
                                "1959111\n"
                                "809597\n"
                                "2251189\n"
                                "537705\n"
                                "929584\n"
                                "506737\n"
                                "708895\n"
                                "1900790\n"
                                "2553920\n"
                                "1196779\n"
                                "2411446\n"
                                "1002296\n"
                                "1580442\n"
                                "100291\n"
                                "433455\n"
                                "2368043\n"
                                "906984\n")

        self.input2 = StringIO("222:\n")

    # ------------
    # netflix_read
    # ------------

    def test_read_1(self):
        x = netflix_read(self.input1)
        self.assertEqual(list(x.keys())[0], 1000)

    # ------------
    # netflix_eval
    # ------------

    def test_eval_1(self):
        input_dict = netflix_read(self.input1)
        predictions_dict = netflix_eval(input_dict)

        self.assertEqual(list(predictions_dict.keys())[0], 1000)

    # ----------------
    # netflix_get_rmse
    # ----------------

    def test_get_rmse(self):
        predictions_dict = {1: {1: 3, 2: 3}}
        correct_ratings  = {1: {1: 3, 2: 3}}

        self.assertEqual(netflix_get_rmse(correct_ratings, predictions_dict), 0)

    # -------------
    # netflix_print
    # -------------

    def test_print(self):
        predictions_dict = {1: {1: 3, 2: 3}}

        w = StringIO()
        netflix_print(w, predictions_dict)
        self.assertEqual(w.getvalue(), "1:\n3.00\n3.00\n")

    # -------------
    # netflix_solve
    # -------------


# ----
# main
# ----

if __name__ == "__main__" :
    main()