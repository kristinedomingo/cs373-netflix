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

        self.input_small = StringIO("9997:\n2179700\n1347835\n765578\n2328701\n")

        self.input_small2 = StringIO("9996:\n66828\n1149582\n336696\n2462908\n1589627\n1720226"
                                        "\n1194354\n592532\n1351081\n80354\n16792\n481320\n899431"
                                        "\n570792\n1619158\n2571420\n1817485\n1206224\n1553993\n")

        self.input_small3 = StringIO("9998:\n1288730\n1107317\n2536567\n")

    # ------------
    # netflix_read
    # ------------

    def test_read_1(self):
        x = netflix_read(self.input1, [])
        self.assertEqual(list(x.keys())[0], 1000)

    # ------------
    # netflix_eval
    # ------------

    def test_eval_1(self):
        input_dict = netflix_read(self.input1, [])
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

    def test_print_1(self):
        predictions_dict = {1: {1: 3, 2: 3}}

        w = StringIO()
        netflix_print(w, predictions_dict, [1])
        self.assertEqual(w.getvalue(), "1:\n3.00\n3.00\n")

    def test_print_2(self):
        predictions_dict = {10: {400: 34, 54: 56}}

        w = StringIO()
        netflix_print(w, predictions_dict, [10])
        self.assertEqual(w.getvalue(), "10:\n34.00\n56.00\n")

    def test_print_3(self):
        predictions_dict = {101: {20: 4, 7: 3, 5: 3}}

        w = StringIO()
        netflix_print(w, predictions_dict, [101])
        self.assertEqual(w.getvalue(), "101:\n4.00\n3.00\n3.00\n")

    def test_print_4(self):
        predictions_dict = {102: {43: 4, 4: 1, 6: 2}}

        w = StringIO()
        netflix_print(w, predictions_dict, [102])
        self.assertEqual(w.getvalue(), "102:\n4.00\n1.00\n2.00\n")

    # -------------
    # netflix_solve
    # -------------

    def test_solve_1(self):
        w = StringIO()
        netflix_solve(self.input_small, w)
        self.assertEqual(w.getvalue(), "9997:\n3.72\n3.79\n3.62\n3.91\nRMSE: 1.00")

    def test_solve_2(self):
        w = StringIO()
        netflix_solve(self.input_small2, w)
        self.assertEqual(w.getvalue(), "9996:\n2.43\n2.85\n3.56\n3.57\n3.76\n3.02\n4.10\n3.22\n2.97"
            "\n2.86\n3.05\n2.89\n3.72\n3.56\n2.56\n2.84\n3.02\n4.16\n3.35\nRMSE: 1.57")

    def test_solve_3(self):
        w = StringIO()
        netflix_solve(self.input_small3, w)
        self.assertEqual(w.getvalue(), "9998:\n2.72\n3.57\n2.95\nRMSE: 1.04")


# ----
# main
# ----

if __name__ == "__main__" :
    main()