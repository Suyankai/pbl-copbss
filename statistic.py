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

    fastica = pd.read_csv("tmp/fastica.csv", header=None).values
    meica = pd.read_csv("tmp/meica.csv", header=None).values
    aeica = pd.read_csv("tmp/aeica.csv", header=None).values

    source_number = fastica[:, 0].astype(int)
    snr_fastica = source_number
    time_fastica = source_number
    snr_meica = source_number
    time_meica = source_number
    snr_aeica = source_number
    time_aeica = source_number
    test_round = 30
    for i in range(test_round):
        snr_fastica = np.c_[snr_fastica, fastica[:, 1+i*2]]
        time_fastica = np.c_[time_fastica, fastica[:, 2+i*2]]
        snr_meica = np.c_[snr_meica, meica[:, 1+i*2]]
        time_meica = np.c_[time_meica, meica[:, 2+i*2]]
        snr_aeica = np.c_[snr_aeica, aeica[:, 1+i*2]]
        time_aeica = np.c_[time_aeica, aeica[:, 2+i*2]]

    snr_fastica_stat = []
    time_fastica_stat = []
    snr_meica_stat = []
    time_meica_stat = []
    snr_aeica_stat = []
    time_aeica_stat = []
    for i in range(len(source_number)):
        conf_interval_low, conf_interval_high = st.t.interval(0.95, len(snr_fastica[i, 1:])-1, loc=np.mean(snr_fastica[i, 1:]), scale=st.sem(snr_fastica[i, 1:]))
        conf_mean = np.mean(snr_fastica[i, 1:])
        snr_fastica_stat.append([source_number[i], conf_interval_low, conf_mean, conf_interval_high])

        conf_interval_low, conf_interval_high = st.t.interval(0.95, len(time_fastica[i, 1:])-1, loc=np.mean(time_fastica[i, 1:]), scale=st.sem(time_fastica[i, 1:]))
        conf_mean = np.mean(time_fastica[i, 1:])
        time_fastica_stat.append([source_number[i], conf_interval_low, conf_mean, conf_interval_high])

        conf_interval_low, conf_interval_high = st.t.interval(0.95, len(snr_meica[i, 1:])-1, loc=np.mean(snr_meica[i, 1:]), scale=st.sem(snr_meica[i, 1:]))
        conf_mean = np.mean(snr_meica[i, 1:])
        snr_meica_stat.append([source_number[i], conf_interval_low, conf_mean, conf_interval_high])

        conf_interval_low, conf_interval_high = st.t.interval(0.95, len(time_meica[i, 1:])-1, loc=np.mean(time_meica[i, 1:]), scale=st.sem(time_meica[i, 1:]))
        conf_mean = np.mean(time_meica[i, 1:])
        time_meica_stat.append([source_number[i], conf_interval_low, conf_mean, conf_interval_high])

        conf_interval_low, conf_interval_high = st.t.interval(0.95, len(snr_aeica[i, 1:])-1, loc=np.mean(snr_aeica[i, 1:]), scale=st.sem(snr_aeica[i, 1:]))
        conf_mean = np.mean(snr_aeica[i, 1:])
        snr_aeica_stat.append([source_number[i], conf_interval_low, conf_mean, conf_interval_high])

        conf_interval_low, conf_interval_high = st.t.interval(0.95, len(time_aeica[i, 1:])-1, loc=np.mean(time_aeica[i, 1:]), scale=st.sem(time_aeica[i, 1:]))
        conf_mean = np.mean(time_aeica[i, 1:])
        time_aeica_stat.append([source_number[i], conf_interval_low, conf_mean, conf_interval_high])

    save_data_csv(snr_fastica_stat, 'tmp/snr_fastica_stat.csv')
    save_data_csv(time_fastica_stat, 'tmp/time_fastica_stat.csv')
    save_data_csv(snr_meica_stat, 'tmp/snr_meica_stat.csv')
    save_data_csv(time_meica_stat, 'tmp/time_meica_stat.csv')
    save_data_csv(snr_aeica_stat, 'tmp/snr_aeica_stat.csv')
    save_data_csv(time_aeica_stat, 'tmp/time_aeica_stat.csv')
