[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Overview of Noval ICA
This project includes on-going research on Blind Source Separation (BSS) as following:
- MeICA: multi-level extraction
- CdICA: component dependent
- AeICA: adaptive extraction
- UfICA: aeica + cdica

The implementation is based on FastICA in [scikit-learn](https://scikit-learn.org/stable/). 

# Required packages
- numpy
- scipy
- museval
- progressbar2
- ffmpeg

These could be installed by `conda install numpy scipy museval progressbar2 ffmpeg`, if the environment is managed by Anaconda.

# Key codes
- pyfastbss_core.py: core analysis.
- pyfastbss_testbed.py: files read/write, data pre-processing, and evaluation tool.
- pyfastbss_example.py: simulation setup and data measurement.

# Citation

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
# About Us

We are researchers at the Deutsche Telekom Chair of Communication Networks (ComNets) at TU Dresden, Germany. Our focus is on in-network computing.

* **Huanzhuo Wu** - huanzhuo.wu@tu-dresden.de
* **Yunbin Shen** - yunbin.shen@mailbox.tu-dresden.de

# License

This project is licensed under the [MIT license](./LICENSE).

# To-do
