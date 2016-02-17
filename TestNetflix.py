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

        self.input2 = StringIO("222:\n10000")
        self.input3 = StringIO("1:\n")

        self.input_small = StringIO("9997:\n2179700\n1347835\n765578\n2328701\n")

    # ------------
    # netflix_read
    # ------------

    def test_read_1(self):
        x = netflix_read(self.input1, [])
        self.assertEqual(list(x.keys())[0], 1000)
        self.assertEqual(x[1000][0], 2326571)
        self.assertEqual(x[1000][26], 906984)

    def test_read_2(self):
        x = netflix_read(self.input2, [])
        self.assertEqual(list(x.keys())[0], 222)
        self.assertEqual(x[222][0], 10000)

    def test_read_3(self):
        x = netflix_read(self.input3, [])
        self.assertEqual(list(x.keys())[0], 1)

    # ------------
    # netflix_eval
    # ------------

    def test_eval_1(self):
        input_dict = netflix_read(self.input1, [])
        predictions_dict = netflix_eval(input_dict)
        self.assertEqual(list(predictions_dict.keys())[0], 1000)
        self.assertEqual(round(predictions_dict[1000][2326571], 2), 3.18)

    def test_eval_2(self):
        input_dict = netflix_read(self.input1, [])
        predictions_dict = netflix_eval(input_dict)
        self.assertEqual(round(predictions_dict[1000][2251189], 2), 3.18)
        self.assertEqual(round(predictions_dict[1000][2368043], 2), 3.03)
        self.assertEqual(round(predictions_dict[1000][929584], 2), 3.86)

    def test_eval_3(self):
        input_dict = netflix_read(self.input1, [])
        predictions_dict = netflix_eval(input_dict)
        self.assertEqual(round(predictions_dict[1000][1900790], 2), 2.97)
        self.assertEqual(round(predictions_dict[1000][1960212], 2), 3.21)
        self.assertEqual(round(predictions_dict[1000][79755], 2), 3.71)

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
        netflix_print(w, predictions_dict, [1])
        self.assertEqual(w.getvalue(), "1:\n3.00\n3.00\n")

    # -------------
    # netflix_solve
    # -------------

    def test_solve(self):
        w = StringIO()
        netflix_solve(self.input_small, w)
        self.assertEqual(w.getvalue(), "9997:\n3.72\n3.79\n3.62\n3.91\nRMSE: 1.00")


# ----
# main
# ----

if __name__ == "__main__" :
    main()