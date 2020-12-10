from pyfastbss_core import PyFastbss, pyfbss
from pyfastbss_testbed import pyfbss_tb
import pyfastbss_example as pyfbss_ex
import numpy as np
import os
import math
import progressbar
PGB = progressbar.ProgressBar()

if __name__ == "__main__":
    # TODO: 接受controller的X,生成B

    # 这个节点用来处理B矩阵，首先生成一个初始化的B
    X=0
    B1 = pyfbss.generate_initial_matrix_B(X)
    pass