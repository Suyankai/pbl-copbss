from pyfastbss_core import PyFastbss, pyfbss
from pyfastbss_testbed import pyfbss_tb
import pyfastbss_example as pyfbss_ex
import numpy as np
import os
import math
import progressbar
PGB = progressbar.ProgressBar()

if __name__ == '__main__':

    folder_address = 'google_dataset/32000_wav_factory'
    duration = 5
    extraction_base = 2

    Eve_MeICA = []

    for source_number in np.arange(2, 5, 1):
        tmp_meica = [source_number]
    
        for test_i in np.arange(1, 2, 1):
            S, A, X = pyfbss_tb.generate_matrix_S_A_X(
                folder_address, duration, source_number, mixing_type="normal", max_min=(1, 0.01), mu_sigma=(0, 1))
            print('type        eval_dB            time(ms) for       ' +
                str(source_number)+' sources, ' + str(test_i) + '-th test.')
            print(
                '--------------------------------------------------------------------------------')
            eval_type = 'sdr'

    # Time and accuracy of MeICA
            pyfbss_tb.timer_start()
            hat_S = pyfbss.meica(X, max_iter=100, tol=1e-04,
                                break_coef=0.92, ext_multi_ica=extraction_base)
            time = pyfbss_tb.timer_value()
            Eval_dB = pyfbss_tb.bss_evaluation(S, hat_S, eval_type)
            tmp_meica.extend([Eval_dB, time])
            print('MeICA:   ', Eval_dB, '; ', time)
    
        Eve_MeICA.append(tmp_meica)
    pyfbss_ex.save_data_csv(Eve_MeICA, 'test_results/google_dataset/meica.csv')