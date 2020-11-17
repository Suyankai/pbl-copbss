This project includes all improved fastica algorithms for cooperative Blind Source Separation (BSS) based on FastICA algorithm.
- meica: multi-level extraction
- cdica: component dependent
- aeica: adaptive extraction
- ufica: aeica + cdica

# Required packages:
- numpy
- scipy
- museval
- progressbar2
- ffmpeg

These could be installed by 'conda install numpy scipy museval progressbar2 ffmpeg', if the eviroment is managed by Anaconda.

# Key codes:
- pyfastbss_core.py
  - core analysis.
- pyfastbss_testbed.py
  - files read/write and data pre-processing.
- pyfastbss_example.py
  - simulation setup and data measurement.

# To-do:
- update 'statistic.py'
- add reference papers
