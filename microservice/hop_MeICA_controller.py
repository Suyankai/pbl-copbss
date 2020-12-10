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
