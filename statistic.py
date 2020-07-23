import numpy as np
import pandas as pd
import scipy.stats as st
import os.path

def save_data_csv(data, name_csv):
    if os.path.isfile(name_csv):
        f = open(file=name_csv, mode='ab')
        np.savetxt(f, data, fmt='%1.4f', delimiter=",")
        f.close()
    else:
        np.savetxt(name_csv, data, fmt='%1.4f', delimiter=",")

if __name__ == '__main__':

    fastica = pd.read_csv("test_results/fastica.csv", header=None).values
    cdica = pd.read_csv("test_results/cdica.csv", header=None).values
    ufica = pd.read_csv("test_results/ufica.csv", header=None).values

    source_number = fastica[:, 0].astype(int)
    snr_fastica = source_number
    time_fastica = source_number
    snr_cdica = source_number
    time_cdica = source_number
    snr_ufica = source_number
    time_ufica = source_number
    test_round = 30
    for i in range(test_round):
        snr_fastica = np.c_[snr_fastica, fastica[:, 1+i*2]]
        time_fastica = np.c_[time_fastica, fastica[:, 2+i*2]]
        snr_cdica = np.c_[snr_cdica, cdica[:, 1+i*2]]
        time_cdica = np.c_[time_cdica, cdica[:, 2+i*2]]
        snr_ufica = np.c_[snr_ufica, ufica[:, 1+i*2]]
        time_ufica = np.c_[time_ufica, ufica[:, 2+i*2]]

    snr_fastica_stat = []
    time_fastica_stat = []
    snr_cdica_stat = []
    time_cdica_stat = []
    snr_ufica_stat = []
    time_ufica_stat = []
    for i in range(len(source_number)):
        conf_interval_low, conf_interval_high = st.t.interval(0.95, len(snr_fastica[i, 1:])-1, loc=np.mean(snr_fastica[i, 1:]), scale=st.sem(snr_fastica[i, 1:]))
        conf_mean = np.mean(snr_fastica[i, 1:])
        snr_fastica_stat.append([conf_interval_low, conf_mean, conf_interval_high])

        conf_interval_low, conf_interval_high = st.t.interval(0.95, len(time_fastica[i, 1:])-1, loc=np.mean(time_fastica[i, 1:]), scale=st.sem(time_fastica[i, 1:]))
        conf_mean = np.mean(time_fastica[i, 1:])
        time_fastica_stat.append([conf_interval_low, conf_mean, conf_interval_high])

        conf_interval_low, conf_interval_high = st.t.interval(0.95, len(snr_cdica[i, 1:])-1, loc=np.mean(snr_cdica[i, 1:]), scale=st.sem(snr_cdica[i, 1:]))
        conf_mean = np.mean(snr_cdica[i, 1:])
        snr_cdica_stat.append([conf_interval_low, conf_mean, conf_interval_high])

        conf_interval_low, conf_interval_high = st.t.interval(0.95, len(time_cdica[i, 1:])-1, loc=np.mean(time_cdica[i, 1:]), scale=st.sem(time_cdica[i, 1:]))
        conf_mean = np.mean(time_cdica[i, 1:])
        time_cdica_stat.append([conf_interval_low, conf_mean, conf_interval_high])

        conf_interval_low, conf_interval_high = st.t.interval(0.95, len(snr_ufica[i, 1:])-1, loc=np.mean(snr_ufica[i, 1:]), scale=st.sem(snr_ufica[i, 1:]))
        conf_mean = np.mean(snr_ufica[i, 1:])
        snr_ufica_stat.append([conf_interval_low, conf_mean, conf_interval_high])

        conf_interval_low, conf_interval_high = st.t.interval(0.95, len(time_ufica[i, 1:])-1, loc=np.mean(time_ufica[i, 1:]), scale=st.sem(time_ufica[i, 1:]))
        conf_mean = np.mean(time_ufica[i, 1:])
        time_ufica_stat.append([conf_interval_low, conf_mean, conf_interval_high])

    save_data_csv(snr_fastica_stat, 'test_results/snr_fastica_stat.csv')
    save_data_csv(time_fastica_stat, 'test_results/time_fastica_stat.csv')
    save_data_csv(snr_cdica_stat, 'test_results/snr_cdica_stat.csv')
    save_data_csv(time_cdica_stat, 'test_results/time_cdica_stat.csv')
    save_data_csv(snr_ufica_stat, 'test_results/snr_ufica_stat.csv')
    save_data_csv(time_ufica_stat, 'test_results/time_ufica_stat.csv')
