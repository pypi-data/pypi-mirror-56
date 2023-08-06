# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 13:43:18 2018

@author: Stefan
"""

# -*- coding: utf-8 -*-

import numpy as np
from indago.optimizer import Optimizer
import random


class FWA(Optimizer):
    """Firework Algorithm class"""

    def __init__(self):
        """Initialization"""
        super(FWA, self).__init__()

        self.X = None
        self.method = None
        self.params = {}

    def init(self):

        defined_params = list(self.params.keys())
        mandatory_params, optional_params = [], []

        if self.method == 'vanilla':
            mandatory_params = 'n m1 m2'.split()
            optional_params = ''.split()
        elif self.method == '---some modification----':
            mandatory_params = 'a b c'.split()
            optional_params = 'd e'.split()

        for param in mandatory_params:
            # if param not in defined_params:
            #     print('Error: Missing parameter (%s)' % param)
            assert param in defined_params, 'Error: Missing parameter (%s)' % param

        for param in defined_params:
            if param not in mandatory_params and param not in optional_params:
                print('Warning: Excessive parameter (%s)' % param)

        self.X = np.empty([self.params['n'], self.dimensions]) * np.nan
        self.F = np.empty([self.params['n']]) * np.nan

        for p in range(self.params['n']):
            self.X[p, :] = np.random.uniform(self.lb, self.ub)
            self.F[p] = self.objective(self.X[p, :])

        ibest = np.argmin(self.F)
        self.BX = self.X[ibest, :]
        self.BF = self.F[ibest]

    """
    Firework Algorithm
    """

    def run(self, eps=0.001, amp=10, a=0.01, b=10):
        """
        :param n: number of fireworks
        :param function: test function
        :param lb: lower limits for plot axes
        :param ub: upper limits for plot axes
        :param dimension: space dimension
        :param iteration: the number of iterations
        :param m1: parameter controlling the number of normal sparks
    (default value is 7)
        :param m2: parameter controlling the number of Gaussian sparks
    (default value is 7)
        :param eps: constant used to avoid division by zero (default value is 0.001)
        :param amp: amplitude of normal explosion (default value is 2)
        :param a: parameter controlling the lower bound for number of normal sparks
    (default value is 0.3)
        :param b: parameter controlling the upper bound for number of normal sparks,
     b must be greater than a (b is set to 3 by default)
        """

        self.init()

        for i in range(self.iterations):
            fmin = np.min(self.F)
            fmax = np.max(self.F)

            sparks = []
            for p in range(self.params['n']):
                fw = self.X[p, :]

                # Explosion operator
                # self.__explosion_operator(sparks, fw, self.objective, self.dimensions, m1, eps, amp, fmin, fmax, a, b)

                # Number of sparks
                n1 = self.params['m1'] * (fmax - self.F[p] + eps) / \
                    np.sum(fmax - self.F + eps)
                n1 = self.min_max_round(
                    n1, self.params['m1'] * a, self.params['m2'] * b)
                # Amplitude
                A = amp * (self.F[p] - fmin + eps) / \
                    (np.sum(self.F - fmin) + eps)
                # print('n1:', n1, 'A:', A)

                for j in range(n1):
                    sparks.append(np.copy(fw))
                    for k in range(self.dimensions):
                        if (random.choice([True, False])):
                            sparks[-1][k] += random.uniform(-A, A)

                # print('explosion sparks:', len(sparks))

            self.__gaussian_mutation(
                sparks, self.dimensions, self.params['m2'])

            self.__mapping_rule(sparks, self.lb, self.ub, self.dimensions)
            self.__selection(sparks, self.params['n'], self.objective)

            # for p in range(self.swarm_size):
            #     self.F[p] = self.objective(self.X[p,:])

            if np.min(self.F) <= self.BF:
                self.BF = np.min(self.F)
                self.BX = np.copy(self.X[np.argmin(self.F), :])

            # print(i, self.BF, len(sparks))

        return self.BF, self.BX
        # self.best = Gbest
        # self._set_Gbest(Gbest)

    def __explosion_operator(self, sparks, fw, function,
                             dimension, m, eps, amp, Ymin, Ymax, a, b):
        sparks_num = self.__round(m * (Ymax - function(fw) + eps) /
                                  (sum([Ymax - function(fwk) for fwk in self.X]) + eps), m, a, b)
        print(sparks_num)

        amplitude = amp * (function(fw) - Ymax + eps) / \
            (sum([function(fwk) - Ymax for fwk in self.X]) + eps)

        for j in range(int(sparks_num)):
            sparks.append(np.array(fw))
            for k in range(dimension):
                if (random.choice([True, False])):
                    sparks[-1][k] += random.uniform(-amplitude, amplitude)

    def __gaussian_mutation(self, sparks, dimension, m):
        for j in range(m):
            fw = self.X[np.random.randint(self.params['n'])]
            g = np.random.normal(1, 1)
            sparks.append(np.array(fw))
            for k in range(dimension):
                if(random.choice([True, False])):
                    sparks[-1][k] *= g

    def __mapping_rule(self, sparks, lb, ub, dimension):
        for i in range(len(sparks)):
            for j in range(dimension):
                if(sparks[i][j] > ub[j] or sparks[i][j] < lb[j]):
                    sparks[i][j] = lb[j] + \
                        (sparks[i][j] - lb[j]) % (ub[j] - lb[j])

    def __selection(self, sparks, n, function):
        for s in sparks:
            self.X = np.vstack([self.X, s])
            self.F = np.append(self.F, function(s))

        isort = np.argsort(self.F)[:n]
        self.X = self.X[isort, :]
        self.F = self.F[isort]
        # self.X = sorted(np.concatenate((self.X, sparks)), key=function)[:n]

        # print('selection:', self.F[0], self.F[-1], len(sparks))

    def min_max_round(self, s, smin, smax):
        return int(np.round(np.min([np.max([s, smin]), smax])))

    def __round(self, s, m, a, b):
        if (s < a * m):
            return round(a * m)
        elif (s > b * m):
            return round(b * m)
        else:
            return round(s)
