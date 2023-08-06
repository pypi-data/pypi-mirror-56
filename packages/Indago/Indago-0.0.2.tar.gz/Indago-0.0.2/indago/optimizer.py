# -*- coding: utf-8 -*-


class Optimizer:
    """Base class for all optimization methods."""

    def __init__(self):
        """Initialization"""

        self.objective = None
        self.constraints = None
        self.lb = None
        self.ub = None
        self.verbose = None
        self.report = {}
