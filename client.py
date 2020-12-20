from pyfastbss_core import PyFastbss, pyfbss
from pyfastbss_testbed import pyfbss_tb
import pyfastbss_example as pyfbss_ex
import numpy as np
import os
import math
import progressbar
# 引用一些hop节点
from hop_B_Manager import hop_B_Manager
from hop_MeICA_controller import hop_MeICA_controller
import hop_MeICA_newton_iteration
import hop_MeICA_Stack
from hop_Source_controller import hop_Source_controller
PGB = progressbar.ProgressBar()


if __name__ == "__main__":
    # init parameter to generate S
    source_number = 2
    mixing_type = "normal"
    max_min = (1, 0.01)
    mu_sigma = (0, 1)
    folder_address = 'google_dataset/32000_wav_factory'
    duration = 5

    # 用于输出结果的参数
    tmp_meica = [source_number]
    Eve_MeICA = []

    #参数 MeICA
    max_iter = 100
    tol = 1e-04,
    break_coef = 0.92
    ext_multi_ica = 2

    # 计时，输出模板
    pyfbss_tb.timer_start()
    print('type        eval_dB            time(ms) for       ' +str(source_number)+' sources, ' + str(1) + '-th test.')
    print(
        '--------------------------------------------------------------------------------')
    eval_type = 'sdr'

    # 开始算
    Source_controller = hop_Source_controller(
        folder_address, duration, source_number, mixing_type, max_min, mu_sigma)
    B_Manager = hop_B_Manager(Source_controller)
    MeICA_controller = hop_MeICA_controller(
        max_iter, tol, break_coef, ext_multi_ica, Source_controller, B_Manager)
    
    hat_S = MeICA_controller.get_hat_S()
    time = pyfbss_tb.timer_value()
    Eval_dB = pyfbss_tb.bss_evaluation(
        Source_controller.get_S(), hat_S, eval_type)
    tmp_meica.extend([Eval_dB, time])
    print('MeICA:   ', Eval_dB, '; ', time)

    Eve_MeICA.append(tmp_meica)
    pyfbss_ex.save_data_csv(Eve_MeICA, 'test_results/google_dataset/meica.csv')
