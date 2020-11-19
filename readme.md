[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Novel ICA
Blind Source Separation (BSS) is often used to solve the cocktail party problem, which is an attempt to separate a group of source signals from a set of mixed signals.
In general, BSS is used for image, audio, medical EEG, and communication MIMO analysis.
However, in the era of 5G, increasing demand for Ultra-Reliable Low-Latency Communications (URLLC) toward these applications becomes urgent, especially acoustic signal processing in IoT networks. Therefore, this project primarily explores BSS algorithms for URLLC and intends to virtualize it to integrate it into 5G networks.

## Table of Contents

- [Novel ICA](#novel-ica)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Install](#install)
  - [Usage](#usage)
  - [Citation](#citation)
  - [About Us](#about-us)
  - [License](#license)
  - [Todo](#todo)

## Overview
This project contains:
1. FastICA, baseline algorithm from A. Hyvarinen.
2. CdICA, Component-dependent Independent Component Analysis.
3. AeICA, Adaptive-extraction Independent Component Analysis.
4. UfICA, Unified Independent Component Analysis.
5. MeICA, Multi-level Extraction Independent Component Analysis.

The implementation is based on FastICA in [scikit-learn](https://scikit-learn.org/stable/). 

## Install 
This project uses Python. Following packages are required:
- numpy
- scipy
- museval
- progressbar2
- ffmpeg

These could be installed by `conda install numpy scipy museval progressbar2 ffmpeg`, if the environment is managed by Anaconda.

A test data set from [Google Audio Set](https://research.google.com/audioset/) is provided for testing.

## Usage 
The core analysis algorithm is given in `pyfastbss_core.py`.

Signal reading and writing, as well as data pre-processing and evaluation, are done by `pyfastbss_testbed.py`.

Testing setup can be done in `pyfastbss_example.py`. Test results, including Separation Accuracy and Separation Time, are stored as ***.csv*** in the folder `test_results/google_dataset`. An example of using the algorithm FastICA is given below:
```python
S, A, X = pyfbss_tb.generate_matrix_S_A_X(
                folder_address, duration, source_number, mixing_type="normal", max_min=(1, 0.01), mu_sigma=(0, 1))
eval_type = 'sdr'

pyfbss_tb.timer_start()
hat_S = pyfbss.fastica(X, max_iter=100, tol=1e-04)
time = pyfbss_tb.timer_value()
Eval_dB = pyfbss_tb.bss_evaluation(S, hat_S, eval_type)
print('FastICA: ', Eval_dB, '; ', time)
```

Test data set is in the fold `google_dataset`. More data set can be downloaded by using the tool ***Youtube Downloader*** in `youtube_downloader`

## Citation

If you like our repository, please cite our papers.

``` 
@INPROCEEDINGS{Wu2006:Component,
AUTHOR="Huanzhuo Wu and Yunbin Shen and Jiajing Zhang and Ievgenii Anatolijovuch Tsokalo and Hani Salah and Frank H.P. Fitzek",
TITLE="{Component-Dependent} Independent Component Analysis for {Time-Sensitive} Applications",
BOOKTITLE="2020 IEEE International Conference on Communications (ICC): SAC Internet of Things Track (IEEE ICC'20 - SAC-06 IoT Track)",
ADDRESS="Dublin, Ireland",
DAYS=6,
MONTH=jun,
YEAR=2020
}
```

```
@INPROCEEDINGS{Wu2012:Adaptive,
AUTHOR="Huanzhuo Wu and Yunbin Shen and Jiajing Zhang and Hani Salah and Ievgenii Anatolijovuch Tsokalo and Frank H.P. Fitzek",
TITLE="Adaptive {Extraction-Based} Independent Component Analysis for {Time-Sensitive} Applications",
BOOKTITLE="2020 IEEE Global Communications Conference: Selected Areas in Communications: Internet of Things and Smart Connected Communities (Globecom2020 SAC IoTSCC)",
ADDRESS="Taipei, Taiwan",
DAYS=6,
MONTH=dec,
YEAR=2020,
KEYWORDS="Blind source separation; Independent component analysis; Time-sensitive application; IoT"
}
```
## About Us

We are researchers at the Deutsche Telekom Chair of Communication Networks (ComNets) at TU Dresden, Germany. Our focus is on in-network computing.

* **Huanzhuo Wu** - huanzhuo.wu@tu-dresden.de
* **Yunbin Shen** - yunbin.shen@mailbox.tu-dresden.de

## License

This project is licensed under the [MIT license](./LICENSE).

## Todo
