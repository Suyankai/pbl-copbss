import numpy as np
import pandas as pd
import scipy.stats as st
import os.path
import matplotlib
print(matplotlib.get_configdir())
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import mpl_toolkits.axisartist as axisartist

# fastica = pd.read_csv("fastica.csv", header=None).values
# cdica = pd.read_csv("cdica.csv", header=None).values
# ufica = pd.read_csv("ufica.csv", header=None).values

snr_fastica = pd.read_csv("test_results/snr_fastica_stat.csv", header=None).values
time_fastica = pd.read_csv("test_results/time_fastica_stat.csv", header=None).values
snr_cdica = pd.read_csv("test_results/snr_cdica_stat.csv", header=None).values
time_cdica = pd.read_csv("test_results/time_cdica_stat.csv", header=None).values
snr_ufica = pd.read_csv("test_results/snr_ufica_stat.csv", header=None).values
time_ufica = pd.read_csv("test_results/time_ufica_stat.csv", header=None).values
source_number = np.arange(3, 31, 1)
    

reduce_time = time_cdica[1:, 1] / time_fastica[1:, 1] * 100
labels = source_number
#x = np.arange(len(labels))

with plt.style.context(['science', 'ieee']):
    fig = plt.figure(figsize=(5, 5/2))
    width = 0.35
    ax = fig.add_subplot(1,1,1)

    ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    rects1 = ax.bar(labels - width/2, snr_fastica[1:, 1], width, color=(0/256, 114/256, 189/256))
    rects2 = ax.bar(labels + width/2, snr_cdica[1:, 1], width, color=(237/256, 177/256, 32/256))
    ax.set_xlim([0, 32])
    ax.set_ylim([0, 100])
    ax.set_xlabel(r'Source Number $n$')
    ax.set_ylabel(r'SNR($dB$)')
    # ax.legend([rects1, rects2], ["FastICA", "CdICA"], loc='upper left')

    ax_cp = ax.twinx()
    line1, = ax_cp.plot(labels, reduce_time, color='green', lw=0.5, ls='-', marker='o', ms=3)
    ax_cp.set_xlim([0, 32])
    ax_cp.set_ylim([0, 100])
    ax_cp.set_ylabel(r'$R_t \%$')

    ax_cp.legend([line1, rects1, rects2], ["$R_t$", "FastICA", "CdICA"], loc='upper right')
    ax.grid(axis='y', linewidth=0.2)

    plt.savefig("fbss.pdf", dpi=500, bbox_inches = 'tight')
   
