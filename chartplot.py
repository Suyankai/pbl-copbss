import mpl_toolkits.axisartist as axisartist
import matplotlib.ticker as mtick
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as st
import os.path
import matplotlib

print(matplotlib.get_configdir())

# snr_fastica = pd.read_csv('tmp/snr_fastica_stat.csv', header=None).values
snr_fastica = pd.read_csv('test_results/google_dataset/fastica_accuracy_stat.csv', header=None)
snr_fastica['err'] = snr_fastica.loc[:, 2].sub(snr_fastica.loc[:, 1], axis=0)
snr_fastica = snr_fastica.values
# time_fastica = pd.read_csv('tmp/time_fastica_stat.csv', header=None).values
time_fastica = pd.read_csv('test_results/google_dataset/fastica_time_stat.csv', header=None)
time_fastica['err'] = time_fastica.loc[:, 2].sub(
    time_fastica.loc[:, 1], axis=0)
time_fastica = time_fastica.values

# snr_meica = pd.read_csv('tmp/snr_meica_stat.csv', header=None).values
snr_meica = pd.read_csv('test_results/google_dataset/meica_accuracy_stat.csv', header=None)
snr_meica['err'] = snr_meica.loc[:, 2].sub(snr_meica.loc[:, 1], axis=0)
snr_meica = snr_meica.values
# time_meica = pd.read_csv('tmp/time_meica_stat.csv', header=None).values
time_meica = pd.read_csv('test_results/google_dataset/meica_time_stat.csv', header=None)
time_meica['err'] = time_meica.loc[:, 2].sub(time_meica.loc[:, 1], axis=0)
time_meica = time_meica.values

# snr_aeica = pd.read_csv('tmp/snr_aeica_stat.csv', header=None).values
snr_aeica = pd.read_csv('test_results/google_dataset/aeica_accuracy_stat.csv', header=None)
snr_aeica['err'] = snr_aeica.loc[:, 2].sub(snr_aeica.loc[:, 1], axis=0)
snr_aeica = snr_aeica.values
# time_aeica = pd.read_csv('tmp/time_aeica_stat.csv', header=None).values
time_aeica = pd.read_csv('test_results/google_dataset/aeica_time_stat.csv', header=None)
time_aeica['err'] = time_aeica.loc[:, 2].sub(time_aeica.loc[:, 1], axis=0)
time_aeica = time_aeica.values

source_number = np.arange(2, 25, 2)

reduce_time_mefast = time_meica[:, 2] / time_fastica[:, 2] * 100
reduce_time_aefast = time_aeica[:, 2] / time_fastica[:, 2] * 100
labels = source_number

with plt.style.context(['science', 'ieee']):
    fig_width = 6.5
    barwidth = 0.45
    colordict = {
        'meica': '#0077BB',
        'aeica': '#DDAA33',
        'fastica': '#009988'
    }

    plt.rcParams.update({'font.size': 10})

    fig = plt.figure(figsize=(fig_width, fig_width / 1.618))
    ax = fig.add_subplot(1, 1, 1)
    ax.yaxis.grid(True, linestyle='--', which='major', color='lightgrey', alpha=0.5, linewidth=0.2)
    rects1 = ax.bar(labels - barwidth, snr_meica[:12, 1], barwidth, yerr=snr_meica[:12, -1], error_kw=dict(lw=1, capsize=1, capthick=1), fill=True, color=colordict['meica'], ecolor='#555555', alpha=0.95)
    rects2 = ax.bar(labels, snr_aeica[:12, 1], barwidth, yerr=snr_aeica[:12, -1], error_kw=dict(lw=1, capsize=1, capthick=1), fill=True, color=colordict['aeica'], ecolor='#555555', alpha=0.95)
    rects3 = ax.bar(labels + barwidth, snr_fastica[:12, 1], barwidth, yerr=snr_fastica[:12, -1], error_kw=dict(lw=1, capsize=1, capthick=1), fill=True, color=colordict['fastica'], ecolor='#555555', alpha=0.95)
    ax.set_xticks(np.arange(0, 26, 5))
    ax.set_yticks(np.arange(0, 71, 20))
    ax.set_xlim(0, 26)
    ax.set_xlabel(r'Source Number $n$')
    ax.set_ylabel(r'SDR ($dB$)')
    ax.legend([rects1, rects2, rects3], [
              'MeICA', 'AeICA', 'FastICA'], loc='upper right')
    plt.savefig('test_results/bss_sdr.pdf', dpi=600, bbox_inches='tight')

    fig_2 = plt.figure(figsize=(fig_width, fig_width / 1.618))
    ax_2 = fig_2.add_subplot(1, 1, 1)
    ax_2.yaxis.grid(True, linestyle='--', which='major', color='lightgrey', alpha=0.5, linewidth=0.2)
    # line1 = ax_2.errorbar(labels, time_meica[:12, 1], yerr=time_meica[:12, -1], capsize=1, color=colordict['meica'], lw=1, ls='-', marker='o', ms=3)
    line1 = ax_2.errorbar(labels, time_meica[:12, 1], color=colordict['meica'], lw=1, ls='-', marker='o', ms=3)
    line1_fill = ax_2.fill_between(labels, time_meica[:12, 1]-time_meica[:12, -1], time_meica[:12, 1]+time_meica[:12, -1], color=colordict['meica'], alpha=0.2)
    # line2 = ax_2.errorbar(labels, time_aeica[:12, 1], yerr=time_aeica[:12, -1], capsize=1, color=colordict['aeica'], lw=1, ls='-', marker='s', ms=3)
    line2 = ax_2.errorbar(labels, time_aeica[:12, 1], color=colordict['aeica'], lw=1, ls='-', marker='s', ms=3)
    line2_fill = ax_2.fill_between(labels, time_aeica[:12, 1]-time_aeica[:12, -1], time_aeica[:12, 1]+time_aeica[:12, -1], color=colordict['aeica'], alpha=0.2)
    # line3 = ax_2.errorbar(labels, time_fastica[:12, 1], yerr=time_fastica[:12, -1], capsize=1, color=colordict['fastica'], lw=1, ls='-', marker='x', ms=3)
    line3 = ax_2.errorbar(labels, time_fastica[:12, 1], color=colordict['fastica'], lw=1, ls='-', marker='x', ms=3)
    line3_fill = ax_2.fill_between(labels, time_fastica[:12, 1]-time_fastica[:12, -1], time_fastica[:12, 1]+time_fastica[:12, -1], color=colordict['fastica'], alpha=0.2)
    ax_2.set_xticks(np.arange(0, 26, 5))
    ax_2.set_yticks(np.arange(0, 10001, 100))
    plt.yscale('log')
    ax_2.set_xlim(0, 26)
    ax_2.set_xlabel(r'Source Number $n$')
    ax_2.set_ylabel(r'Time ($ms$)')
    ax_2.legend([line1, line2, line3], [
                'MeICA', 'AeICA', 'FastICA'], loc='upper left')
    plt.savefig('test_results/bss_time.pdf', dpi=600, bbox_inches='tight')