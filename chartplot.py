import numpy as np
import pandas as pd
import scipy.stats as st
import os.path
import matplotlib

print(matplotlib.get_configdir())
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import mpl_toolkits.axisartist as axisartist

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

source_number = np.arange(2, 21, 5)

reduce_time_mefast = time_meica[:, 1] / time_fastica[:, 1] * 100
reduce_time_aefast = time_aeica[:, 1] / time_fastica[:, 1] * 100
labels = source_number

with plt.style.context(['science', 'ieee']):
    fig = plt.figure(figsize=(5, 10 / 1.618))
    width = 0.4

    ax = fig.add_subplot(2, 1, 1)
    ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    rects1 = ax.bar(labels - width, snr_meica[:, 1], width, color=(237 / 256, 177 / 256, 32 / 256))
    rects2 = ax.bar(labels, snr_aeica[:, 1], width, color=(0 / 256, 114 / 256, 189 / 256))
    rects3 = ax.bar(labels + width, snr_fastica[:, 1], width, color='black')
    # ax.set_xlim([0, 20])
    # ax.set_ylim([0, 100])
    ax.set_xticks(np.arange(0, 21, 5))
    ax.set_yticks(np.arange(0, 101, 20))
    ax.set_xlabel(r'Source Number $n$')
    ax.set_ylabel(r'SDR ($dB$)')
    ax.legend([rects1, rects2, rects3], ['MeICA', 'AeICA', 'FastICA'], loc='upper left')
    ax.grid(axis='y', linewidth=0.2)

    ax_2 = fig.add_subplot(2, 1, 2)
    ax_2.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    #line1, = ax_2.plot(labels, time_meica[:, 1], color=(237 / 256, 177 / 256, 32 / 256), lw=1, ls='-', marker='o', ms=3)
    #line2, = ax_2.plot(labels, time_aeica[:, 1], color=(0 / 256, 114 / 256, 189 / 256), lw=1, ls='-', marker='s', ms=3)
    # line3, = ax_2.plot(labels, time_fastica[:, 1], color='black', lw=1, ls='-', marker='x', ms=3)
    line1 = ax_2.errorbar(labels, time_meica[:, 1], yerr=time_meica[:, -1], color=(237 / 256, 177 / 256, 32 / 256), lw=1, ls='-', marker='o', ms=3)
    line2 = ax_2.errorbar(labels, time_aeica[:, 1], yerr=time_aeica[:, -1], color=(0 / 256, 114 / 256, 189 / 256), lw=1, ls='-', marker='s', ms=3)
    line3 = ax_2.errorbar(labels, time_fastica[:, 1], yerr=time_fastica[:, -1], color='black', lw=1, ls='-', marker='x', ms=3)
    # ax_2.set_xlim([0, 20])
    # ax_2.set_ylim([0, 700])
    ax_2.set_xticks(np.arange(0, 21, 5))
    ax_2.set_yticks(np.arange(0, 501, 100))
    ax_2.set_xlabel(r'Source Number $n$')
    ax_2.set_ylabel(r'Time ($ms$)')
    ax_2.legend([line1, line2, line3], ['MeICA', 'AeICA', 'FastICA'], loc='upper left')
    ax_2.grid(axis='y', linewidth=0.2)

    plt.savefig('bss.pdf', dpi=500, bbox_inches='tight')
