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
    # TODO 建立socket，接受参数
    
    # 这里面先假设接收到的是2
    source_number=2
    mixing_type="normal"
    max_min=(1, 0.01)
    mu_sigma=(0, 1) 
    folder_address = 'google_dataset/32000_wav_factory'
    duration = 5

    S, A, X = pyfbss_tb.generate_matrix_S_A_X(
                folder_address, duration, source_number, mixing_type="normal", max_min=(1, 0.01), mu_sigma=(0, 1))

    # TODO 传回给client S,A,X