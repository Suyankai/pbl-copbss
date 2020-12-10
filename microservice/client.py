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


if __name__ == "__main__":
    # init parameter to generate S
    source_number=2
    mixing_type="normal"
    max_min=(1, 0.01)
    mu_sigma=(0, 1)
    
    #参数 MeICA
    max_iter=100
    tol=1e-04,
    break_coef=0.92
    ext_multi_ica=2

    # 计时，输出模板
    pyfbss_tb.timer_start()
    print('type        eval_dB            time(ms) for       ' +
                str(source_number)+' sources, ' + 1 + '-th test.')
    print(
        '--------------------------------------------------------------------------------')
    eval_type = 'sdr'
    # TODO: 建立socket

    # TODO: 将这些参数传入hop_getS

    # TODO: 接受SAX

    # TODO: 传入X给meica入口,hop_MEICA_controller

    
    # TODO: 最后再处理，接收B


