#!/usr/bin/env python3

# -------------------------------
# projects/netflix/TestNetflix.py
# Copyright (C) 2015
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

        prediction = float(str(predictions_dict[1000][2326571])[:4])
        self.assertEqual(prediction, 3.22)

    def test_eval_2(self):
        input_dict = netflix_read(self.input1, [])
        predictions_dict = netflix_eval(input_dict)

        prediction = float(str(predictions_dict[1000][2251189])[:4])
        self.assertEqual(prediction, 3.06)

        prediction = float(str(predictions_dict[1000][2368043])[:4])
        self.assertEqual(prediction, 2.87)

        prediction = float(str(predictions_dict[1000][929584])[:4])
        self.assertEqual(prediction, 3.93)

    def test_eval_3(self):
        input_dict = netflix_read(self.input1, [])
        predictions_dict = netflix_eval(input_dict)

        prediction = float(str(predictions_dict[1000][977808])[:4])
        self.assertEqual(prediction, 2.77)

        prediction = float(str(predictions_dict[1000][1960212])[:4])
        self.assertEqual(prediction, 3.2)

        prediction = float(str(predictions_dict[1000][79755])[:4])
        self.assertEqual(prediction, 3.77)

    # ----------------
    # netflix_get_rmse
    # ----------------

    def test_get_rmse_1(self):
        predictions_dict = {1: {1: 3, 2: 3}}
        correct_ratings  = {1: {1: 3, 2: 3}}
        self.assertEqual(netflix_get_rmse(correct_ratings, predictions_dict), 0)

    def test_get_rmse_2(self):
        predictions_dict = {1: {1: 3, 2: 3}}
        correct_ratings  = {1: {1: 5, 2: 4}}

        rmse = netflix_get_rmse(correct_ratings, predictions_dict)
        rmse = float(str(rmse)[:4])
        self.assertEqual(rmse, 1.58)

    def test_get_rmse_3(self):
        predictions_dict = {1: {1: 1, 2: 1}}
        correct_ratings  = {1: {1: 5, 2: 5}}

        rmse = netflix_get_rmse(correct_ratings, predictions_dict)
        rmse = float(str(rmse)[:4])
        self.assertEqual(rmse, 4.0)

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
        self.assertEqual(w.getvalue(), "9997:\n3.73\n3.70\n3.93\n3.92\n"
                                       "RMSE: 0.99")

    def test_solve_2(self):
        w = StringIO()
        netflix_solve(self.input_small2, w)
        self.assertEqual(w.getvalue(), "9996:\n2.43\n2.77\n3.67\n3.43\n3.58\n"
                                       "2.96\n4.37\n3.45\n2.94\n3.42\n3.70\n"
                                       "2.60\n3.57\n3.37\n2.56\n3.66\n2.91\n"
                                       "4.23\n3.81\nRMSE: 1.45")

    def test_solve_3(self):
        w = StringIO()
        netflix_solve(self.input_small3, w)
        self.assertEqual(w.getvalue(), "9998:\n2.45\n4.45\n3.45\nRMSE: 0.55")

# ----
# main
# ----

if __name__ == "__main__" :
    main()

""" #pragma: no cover
coverage3 run    --branch TestNetflix.py >  TestNetflix.tmp 2>&1
coverage3 report -m --omit=/lusr/lib/python3.4/dist-packages/*,/home/travis/virtualenv/python3.4.2/lib/python3.4/site-packages/* >> TestNetflix.tmp
cat TestNetflix.tmp
................
----------------------------------------------------------------------
Ran 16 tests in 7.952s

OK
Name             Stmts   Miss Branch BrPart  Cover   Missing
------------------------------------------------------------
Netflix.py          75     11     28      6    83%   71-72, 81-82, 90-91, 99-100, 123, 209-210, 65->71, 75->81, 85->90, 94->99, 119->123, 203->209
TestNetflix.py      97      0      2      1    99%   212->-15
------------------------------------------------------------
TOTAL              172     11     30      7    91%   
"""