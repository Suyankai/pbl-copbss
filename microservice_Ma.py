from pyfastbss_core_microservice_Ma import microservice
from pyfastbss_testbed import pyfbss_tb
import numpy as np
import os
import math
'''
# Divide the MultiLevelExtractionICA into several microservices.
# Note: This version is based on the thoughts of Mingyu Ma.
'''

if __name__ == '__main__':
    
    #Initiate the parameters.
    B = 0
    step = 0
    miu = 5#为了实验随意设的
    lim = 0
    
    folder_address = 'google_dataset/32000_wav_factory'
    duration = 5
    extraction_base = 2
    interval = 30
    source_number = 3
   
    #Load the source data.
    S, A, X = pyfbss_tb.generate_matrix_S_A_X(
                folder_address, duration, source_number, mixing_type="normal", max_min=(1, 0.01), mu_sigma=(0, 1))
    
    #Calculate the result in the first host.
    result = microservice.meica_new(X, B, lim, step, miu, max_iter=100, tol=1e-04, break_coef=0.9, ext_multi_ica=8)
    
    #Print the result in the firsrt host.
    B_host1 = result[0]
    lim_host1 = result[1][0]
    step_host1 = result[1][1]
    print(B_host1, lim_host1, step_host1)
    
    
    
    