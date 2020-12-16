import sys
from numpy.lib.utils import source
sys.path.append("..")
from pyfastbss_core import PyFastbss, pyfbss
from pyfastbss_testbed import pyfbss_tb
import pyfastbss_example as pyfbss_ex
import numpy as np
import os
import math
import progressbar
PGB = progressbar.ProgressBar()


def get_B():
    # TODO 这个函数用来向服务器请求B
    B=0
    return B

def sent_B(B,lim,Flag):
    # TODO 这个函数用来向服务器请求B
    # Flag是当前B的状态，0 是未完成，1是完成
    pass

if __name__ == "__main__":
    max_iter=100
    tol=1e-04,
    break_coef=0.92
    _ext_multi_ica=2
    X=0
    # TODO socket要将以上参数接收
    n, m = X.shape
    _grad = int(math.log(m//n, _ext_multi_ica))
    _prop_series = _ext_multi_ica**np.arange(_grad, -1, -1)
    for i in range(1, _grad+1):
        _X = X[:, ::_prop_series[i]]
        _X, V, V_inv = pyfbss_tb.whiten_with_inv_V(_X)
        sent_B( pyfbss_tb.decorrelation(np.dot(get_B(), V_inv)) , )
        # pyfbss_tb.Stack = []

        B_temp,lim= pyfbss_tb.newton_iteration_auto_break(
            get_B(), _X, max_iter, tol, break_coef)[0]   
        B_temp = np.dot(B_temp, V)
        if i == _grad:
            sent_B(B_temp,lim,1)
        else :
            sent_B(B_temp,lim,0)


