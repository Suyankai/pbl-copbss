import mpl_toolkits.axisartist as axisartist
import matplotlib.ticker as mtick
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as st
import os.path
import matplotlib

print(matplotlib.get_configdir())

snr_fastica = pd.read_csv('test_results/snr_fastica_stat.csv', header=None).values
# time_fastica = pd.read_csv('test_results/time_fastica_stat.csv', header=None).values
time_fastica = pd.read_csv('test_results/time_fastica_stat.csv', header=None)
time_fastica['err'] = time_fastica.loc[:, 1].sub(time_fastica.loc[:, 0], axis=0)
time_fastica = time_fastica.values

snr_meica = pd.read_csv('test_results/snr_meica_stat.csv', header=None).values
# time_meica = pd.read_csv('test_results/time_meica_stat.csv', header=None).values
time_meica = pd.read_csv('test_results/time_meica_stat.csv', header=None)
time_meica['err'] = time_meica.loc[:, 1].sub(time_meica.loc[:, 0], axis=0)
time_meica = time_meica.values

snr_aeica = pd.read_csv('test_results/snr_aeica_stat.csv', header=None).values
# time_aeica = pd.read_csv('test_results/time_aeica_stat.csv', header=None).values
time_aeica = pd.read_csv('test_results/time_aeica_stat.csv', header=None)
time_aeica['err'] = time_aeica.loc[:, 1].sub(time_aeica.loc[:, 0], axis=0)
time_aeica = time_aeica.values

source_number = np.arange(2, 21, 1)

reduce_time_mefast = time_meica[:, 1] / time_fastica[:, 1] * 100
reduce_time_aefast = time_aeica[:, 1] / time_fastica[:, 1] * 100
labels = source_number

with plt.style.context(['science', 'ieee']):
    fig_width = 6.5
    barwidth = 0.25
    colordict = {
        'meica': '#CCBB44',
        'aeica': '#4477AA',
        'fastica': '#000000'
    }

    plt.rcParams.update({'font.size': 10})

    fig = plt.figure(figsize=(fig_width, fig_width / 1.618))
    ax = fig.add_subplot(1, 1, 1)
    ax.yaxis.grid(True, linestyle='--', which='major', color='lightgrey', alpha=0.5, linewidth=0.2)
    rects1 = ax.bar(labels - barwidth, snr_meica[:, 1], barwidth, color=colordict['meica'])
    rects2 = ax.bar(labels, snr_aeica[:, 1], barwidth, color=colordict['aeica'])
    rects3 = ax.bar(labels + barwidth, snr_fastica[:, 1], barwidth, color=colordict['fastica'])
    ax.set_xticks(np.arange(0, 21, 5))
    ax.set_yticks(np.arange(0, 101, 20))
    ax.set_xlabel(r'Source Number $n$')
    ax.set_ylabel(r'SDR ($dB$)')
    ax.legend([rects1, rects2, rects3], ['MeICA', 'AeICA', 'FastICA'], loc='upper left')
    plt.savefig('bss_sdr.pdf', dpi=600, bbox_inches='tight')

    fig_2 = plt.figure(figsize=(fig_width, fig_width / 1.618))
    ax_2 = fig_2.add_subplot(1, 1, 1)
    ax_2.yaxis.grid(True, linestyle='--', which='major', color='lightgrey', alpha=0.5, linewidth=0.2)
    line1 = ax_2.errorbar(labels, time_meica[:, 1], yerr=time_meica[:, -1], color=colordict['meica'], lw=1, ls='-', marker='o', ms=3)
    line2 = ax_2.errorbar(labels, time_aeica[:, 1], yerr=time_aeica[:, -1], color=colordict['aeica'], lw=1, ls='-', marker='s', ms=3)
    line3 = ax_2.errorbar(labels, time_fastica[:, 1], yerr=time_fastica[:, -1], color=colordict['fastica'], lw=1, ls='-', marker='x', ms=3)
    ax_2.set_xticks(np.arange(0, 21, 5))
    ax_2.set_yticks(np.arange(0, 1000, 200))
    ax_2.set_xlabel(r'Source Number $n$')
    ax_2.set_ylabel(r'Time ($ms$)')
    ax_2.legend([line1, line2, line3], ['MeICA', 'AeICA', 'FastICA'], loc='upper left')
    plt.savefig('bss_time.pdf', dpi=600, bbox_inches='tight')
