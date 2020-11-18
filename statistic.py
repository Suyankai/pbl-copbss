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

    fastica = pd.read_csv("test_results/google_dataset/fastica.csv", header=None).values
    meica = pd.read_csv("test_results/google_dataset/meica.csv", header=None).values
    aeica = pd.read_csv("test_results/google_dataset/aeica.csv", header=None).values

    source_number = fastica[:, 0].astype(int)
    accuracy_fastica = source_number
    time_fastica = source_number
    accuracy_meica = source_number
    time_meica = source_number
    accuracy_aeica = source_number
    time_aeica = source_number
    test_round = len(fastica[0, :])//2
    for i in range(test_round):
        accuracy_fastica = np.c_[accuracy_fastica, fastica[:, 1+i*2]]
        time_fastica = np.c_[time_fastica, fastica[:, 2+i*2]]
        accuracy_meica = np.c_[accuracy_meica, meica[:, 1+i*2]]
        time_meica = np.c_[time_meica, meica[:, 2+i*2]]
        accuracy_aeica = np.c_[accuracy_aeica, aeica[:, 1+i*2]]
        time_aeica = np.c_[time_aeica, aeica[:, 2+i*2]]

    accuracy_fastica_stat = []
    time_fastica_stat = []
    accuracy_meica_stat = []
    time_meica_stat = []
    accuracy_aeica_stat = []
    time_aeica_stat = []
    for i in range(len(source_number)):
        conf_interval_low, conf_interval_high = st.t.interval(0.95, len(accuracy_fastica[i, 1:])-1, loc=np.mean(accuracy_fastica[i, 1:]), scale=st.sem(accuracy_fastica[i, 1:]))
        conf_mean = np.mean(accuracy_fastica[i, 1:])
        accuracy_fastica_stat.append([source_number[i], conf_interval_low, conf_mean, conf_interval_high])

        conf_interval_low, conf_interval_high = st.t.interval(0.95, len(time_fastica[i, 1:])-1, loc=np.mean(time_fastica[i, 1:]), scale=st.sem(time_fastica[i, 1:]))
        conf_mean = np.mean(time_fastica[i, 1:])
        time_fastica_stat.append([source_number[i], conf_interval_low, conf_mean, conf_interval_high])

        conf_interval_low, conf_interval_high = st.t.interval(0.95, len(accuracy_meica[i, 1:])-1, loc=np.mean(accuracy_meica[i, 1:]), scale=st.sem(accuracy_meica[i, 1:]))
        conf_mean = np.mean(accuracy_meica[i, 1:])
        accuracy_meica_stat.append([source_number[i], conf_interval_low, conf_mean, conf_interval_high])

        conf_interval_low, conf_interval_high = st.t.interval(0.95, len(time_meica[i, 1:])-1, loc=np.mean(time_meica[i, 1:]), scale=st.sem(time_meica[i, 1:]))
        conf_mean = np.mean(time_meica[i, 1:])
        time_meica_stat.append([source_number[i], conf_interval_low, conf_mean, conf_interval_high])

        conf_interval_low, conf_interval_high = st.t.interval(0.95, len(accuracy_aeica[i, 1:])-1, loc=np.mean(accuracy_aeica[i, 1:]), scale=st.sem(accuracy_aeica[i, 1:]))
        conf_mean = np.mean(accuracy_aeica[i, 1:])
        accuracy_aeica_stat.append([source_number[i], conf_interval_low, conf_mean, conf_interval_high])

        conf_interval_low, conf_interval_high = st.t.interval(0.95, len(time_aeica[i, 1:])-1, loc=np.mean(time_aeica[i, 1:]), scale=st.sem(time_aeica[i, 1:]))
        conf_mean = np.mean(time_aeica[i, 1:])
        time_aeica_stat.append([source_number[i], conf_interval_low, conf_mean, conf_interval_high])

    save_data_csv(accuracy_fastica_stat, 'test_results/google_dataset/fastica_accuracy_stat.csv')
    save_data_csv(time_fastica_stat, 'test_results/google_dataset/fastica_time_stat.csv')
    save_data_csv(accuracy_meica_stat, 'test_results/google_dataset/meica_accuracy_stat.csv')
    save_data_csv(time_meica_stat, 'test_results/google_dataset/meica_time_stat.csv')
    save_data_csv(accuracy_aeica_stat, 'test_results/google_dataset/aeica_accuracy_stat.csv')
    save_data_csv(time_aeica_stat, 'test_results/google_dataset/aeica_time_stat.csv')