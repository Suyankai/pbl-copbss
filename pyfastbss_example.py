from pyfastbss_core import pyfbss
from pyfastbss_testbed import pyfbss_tb
import progressbar
PGB = progressbar.ProgressBar()
'''
# FAST BSS EXAMPLE Version 0.1.0:

    fastica: FastICA (most stable)
    meica: Multi-level extraction ICA (stable)
    cdica: Component dependent ICA (stable)
    aeica: Adaptive extraction ICA (*warning: unstable!)
    ufica: Ultra-fast ICA (cdica + aeica) (*warning: unstable!)

# Basic definition:

    S: Source signals. shape = (source_number, time_slots_number)
    X: Mixed source signals. shape = (source_number, time_slots_number)
    A: Mixing matrix. shape = (source_number, source_number)
    B: Separation matrix. shape = (source_number, source_number)
    hat_S: Estimated source signals durch ICA algorithms. 
        shape = (source_number, time_slots_number)

# Notes:

    X = A @ S
    S = B @ X
    B = A ^ -1
'''


if __name__ == '__main__':

    '''
    # generate_matrix_S_A_X(self, folder_address, wav_range, source_number, 
    # mixing_type="random", max_min=(1, 0.01), mu_sigma=(0, 1)):

    # Usage:

        Generate the mixing matrix S, A, X according to the size of the source 
        signal matrix S

    # Parameters:

        folder_address: Define folder adress, in which the *.wav files exist. 
            The wav files must have only 1 channel.

        duration: The duration of the output original signals, 
            i.e. the whole time domain of the output matrix S

        source number: The number of the source signals in matrix S 

        mixing_type:
            'random': The value of a_i_j are in interval (minimum_value, minimum_value) 
                randomly distributed 
            'normal': The value of a_i_j (i==j) are equal to 1. The value of a_i_j (i!=j) 
                are normal distributed, the distribution correspond with N(mu,sigma) 
                normal distirbution, where the mu is the average value of the a_i,j (i!=j) , 
                and the sigma is the variance of the a_i_j (i!=j).

        max_min: max_min = (minimum_value, minimum_value), are used when the  mixing_type
            is 'random'

        mu_sigma: mu_sigma = (mu, sigma), are used when the mix_type is 'normal'

    # Output:

        Matrix S, A, X.
        The shape of the S and X are (source number, time slots number), 
        the shape of A is (time slots number, time slots number), the wav files are 
        randomly selected to generate the matrix S, A, X.
    '''
    folder_address = '/home/huanzhuo/Documents/NovelICA/wav'
    #folder_address = '/Users/shenyunbin/Documents/Code/fast_bss/10s_wavs'
    duration, source_number = 10, 15
    S, A, X = pyfbss_tb.generate_matrix_S_A_X(
        folder_address, duration, source_number, mixing_type="normal", max_min=(1, 0.01), mu_sigma=(0, 0.1))
    
    print('type             eval_dB             time(ms)')
    print('----------------------------------------------')
    
    eval_type = 'psnr'

    '''
    #Time and snr test for fast ica
    '''
    pyfbss_tb.timer_start()
    hat_S = pyfbss.fastica(X, max_iter=100)
    time = pyfbss_tb.timer_value()
    Eval_dB = pyfbss_tb.bss_evaluation(S, hat_S, eval_type)
    print('fastica', Eval_dB, time)

    '''
    #Time and snr test for multi level extraction ica
    '''
    pyfbss_tb.timer_start()
    hat_S = pyfbss.meica(X, max_iter=100, break_coef=0.92, ext_multi_ica=7)
    time = pyfbss_tb.timer_value()
    Eval_dB = pyfbss_tb.bss_evaluation(S, hat_S, eval_type)
    print('meica ', Eval_dB, time)

    '''
    #time and snr test for component dependent ica
    '''
    pyfbss_tb.timer_start()
    hat_S = pyfbss.cdica(X, max_iter=100, tol=1e-04, ext_initial_matrix=0)
    time = pyfbss_tb.timer_value()
    Eval_dB = pyfbss_tb.bss_evaluation(S, hat_S, eval_type)
    print('cdica ', Eval_dB, time)

    
    '''
    #time and snr test for ultra fast ica
    '''
    pyfbss_tb.timer_start()
    hat_S = pyfbss.aeica(X, max_iter=100, tol=1e-04, ext_adapt_ica=30)
    time = pyfbss_tb.timer_value()
    Eval_dB = pyfbss_tb.bss_evaluation(S, hat_S, eval_type)
    print('aeica', Eval_dB, time)

    '''
    #time and snr test for ultra fast ica
    '''
    pyfbss_tb.timer_start()
    hat_S = pyfbss.ufica(X, max_iter=100, tol=1e-04, ext_initial_matrix=0, ext_adapt_ica=100)
    time = pyfbss_tb.timer_value()
    Eval_dB = pyfbss_tb.bss_evaluation(S, hat_S, eval_type)
    print('ufica ', Eval_dB, time)
