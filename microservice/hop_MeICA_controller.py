import sys
from numpy.lib.utils import source
sys.path.append("..")
from pyfastbss_core import PyFastbss, pyfbss,MultiLevelExtractionICA
from pyfastbss_testbed import pyfbss_tb
import pyfastbss_example as pyfbss_ex
import numpy as np
import os
import math
import progressbar
PGB = progressbar.ProgressBar()

if __name__ == "__main__":
    # TODO 建立socket，接受X

    max_iter=100
    tol=1e-04,
    break_coef=0.92
    ext_multi_ica=2

    # TODO 告诉B.Manager初始化

    # TODO 将参数传递给newton_iteration
        # multi_level_extraction_newton_iteration(self, X, B, max_iter, tol, break_coef, _ext_multi_ica)
