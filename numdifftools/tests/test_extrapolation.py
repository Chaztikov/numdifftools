import unittest
import numpy as np
from numpy.testing import assert_array_almost_equal, assert_allclose
from numdifftools.extrapolation import Dea, dea3, Richardson


class TestRichardson(unittest.TestCase):
    def test_order_step_combinations(self):
        true_vals = {
            (1, 1, 1): [-0.9999999999999998, 1.9999999999999998],
            (1, 1, 2): [-0.33333333333333304, 1.333333333333333],
            (1, 1, 3): [-0.14285714285714307, 1.142857142857143],
            (1, 1, 4): [-0.06666666666666654, 1.0666666666666664],
            (1, 1, 5): [-0.03225806451612906, 1.0322580645161292],
            (1, 1, 6): [-0.015873015873015872, 1.0158730158730154],
            (1, 2, 1): [-0.9999999999999998, 1.9999999999999998],
            (1, 2, 2): [-0.33333333333333304, 1.333333333333333],
            (1, 2, 3): [-0.14285714285714307, 1.142857142857143],
            (1, 2, 4): [-0.06666666666666654, 1.0666666666666664],
            (1, 2, 5): [-0.03225806451612906, 1.0322580645161292],
            (1, 2, 6): [-0.015873015873015872, 1.0158730158730154],
            (2, 1, 1): [0.33333333333333337, -2.0, 2.666666666666667],
            (2, 1, 2): [0.04761904761904753, -0.5714285714285693,
                        1.523809523809522],
            (2, 1, 3): [0.009523809523810024, -0.2285714285714322,
                        1.2190476190476225],
            (2, 1, 4): [0.002150537634408055, -0.10322580645160284,
                        1.1010752688171945],
            (2, 1, 5): [0.0005120327700975248, -0.04915514592935677,
                        1.0486431131592595],
            (2, 1, 6): [0.0001249843769525012, -0.02399700037493191,
                        1.0238720159979793],
            (2, 2, 1): [0.1428571428571428, -1.428571428571427,
                        2.2857142857142843],
            (2, 2, 2): [0.022222222222222185, -0.444444444444444,
                        1.4222222222222216],
            (2, 2, 3): [0.004608294930875861, -0.1843317972350207,
                        1.179723502304145],
            (2, 2, 4): [0.0010582010582006751, -0.08465608465608221,
                        1.0835978835978812],
            (2, 2, 5): [0.0002540005080009476, -0.040640081280166496,
                        1.0403860807721657],
            (2, 2, 6): [6.224712107032182e-05, -0.01991907874258203,
                        1.0198568316215115],
            (3, 1, 1): [-0.04761904761904734, 0.6666666666666641,
                        -2.6666666666666594, 3.047619047619042],
            (3, 1, 2): [-0.003174603174603108, 0.08888888888889318,
                        -0.7111111111111337, 1.6253968253968432],
            (3, 1, 3): [-0.0003072196620577672, 0.01720430107525861,
                        -0.27526881720422713, 1.258371735791026],
            (3, 1, 4): [-3.4135518007183396e-05, 0.003823178016754525,
                        -0.12234169653539884, 1.1185526540366513],
            (3, 1, 5): [-4.031754094968587e-06, 0.0009031129172963892,
                        -0.0577992267083981, 1.056900145545197],
            (3, 1, 6): [-4.901348115149418e-07, 0.00021958039560535103,
                        -0.02810629063481751, 1.0278872003740238],
            (3, 2, 1): [-0.004608294930874168, 0.1935483870967698,
                        -1.5483870967741966, 2.359447004608302],
            (3, 2, 2): [-0.00035273368606647537, 0.02962962962962734,
                        -0.47407407407406155, 1.444797178130501],
            (3, 2, 3): [-3.628578685754835e-05, 0.006096012192020994,
                        -0.19507239014474764, 1.1890126637395837],
            (3, 2, 4): [-4.149808071229888e-06, 0.0013943355119737377,
                        -0.08923747276669802, 1.0878472870627958],
            (3, 2, 5): [-4.970655732572382e-07, 0.0003340280653114369,
                        -0.042755592360228634, 1.0424220613604906],
            (3, 2, 6): [-6.08476257157875e-08, 8.177920896951241e-05,
                        -0.02093547748207586, 1.0208537591207332]}
        for num_terms in [1, 2, 3]:
            for step in [1, 2]:
                for order in range(1, 7):
                    r_extrap = Richardson(step_ratio=2.0, step=step,
                                             num_terms=num_terms, order=order)
                    rule = r_extrap._get_richardson_rule()
                    # print((num_terms, step, order), rule.tolist())
                    assert_array_almost_equal(rule,
                                              true_vals[(num_terms, step,
                                                         order)])
        # self.assert_(False)


class TestExtrapolation(unittest.TestCase):

    def setUp(self):
        n = 7
        Ei = np.zeros(n)
        h = np.zeros(n)
        linfun = lambda i : np.linspace(0, np.pi/2., 2**(i+5)+1)
        for k in np.arange(n):
            x = linfun(k)
            Ei[k] = np.trapz(np.sin(x),x)
            h[k] = x[1]
        self.Ei = Ei
        self.h = h


    def test_dea3_on_trapz_sin(self):
        Ei = self.Ei
        [En, err] = dea3(Ei[0], Ei[1], Ei[2])
        truErr = Ei[:3]-1.
        assert_allclose(truErr,
                        [ -2.00805680e-04, -5.01999079e-05, -1.25498825e-05])
        assert_allclose(En,  1.)
        self.assertLessEqual(err, 0.00021)


    def test_dea_on_trapz_sin(self):
        Ei = self.Ei
        dea_3 = Dea(3)
        for E in Ei:
            En, err = dea_3(E)

        truErr = np.abs(Ei-1.)
        err_bound = 10 * np.array([2.00805680e-04,  5.01999079e-05,
                                   1.25498825e-05, 3.13746471e-06,
                                   7.84365809e-07, 1.96091429e-07,
                                   4.90228558e-08])
        self.assertTrue(np.all(truErr< err_bound))
        assert_allclose(En,  1.)
        self.assertLessEqual(err, 1e-10)

    def test_richardson(self):
        Ei, h = self.Ei[:, np.newaxis], self.h[:, np.newaxis]
        En, err, step = Richardson(step=1, order=1)(Ei, h)
        assert_allclose(En,  1.)
        self.assertTrue(np.all(err<0.0022))


#     def test_epsal():
#         HUGE = 1.E+60
#         TINY = 1.E-60
#         ZERO = 0.E0
#         ONE = 1.E0
#         true_vals = [0.78539816, 0.94805945, 0.99945672]
#         E = []
#         for N, SOFN in enumerate([0.78539816, 0.94805945, 0.98711580]):
#             E.append(SOFN)
#             if N == 0:
#                 ESTLIM = SOFN
#             else:
#                 AUX2 = ZERO
#                 for J in range(N, 0, -1):
#                     AUX1 = AUX2
#                     AUX2 = E[J-1]
#                     DIFF = E[J] - AUX2
#                     if (abs(DIFF) <= TINY):
#                         E[J-1] = HUGE
#                     else:
#                         E[J-1] = AUX1 + ONE/DIFF
#
#                 if (N % 2) == 0:
#                     ESTLIM = E[0]
#                 else:
#                     ESTLIM = E[1]
#             print(ESTLIM, true_vals[N])


if __name__ == "__main__":
    unittest.main()
