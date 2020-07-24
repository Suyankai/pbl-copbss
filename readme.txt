# pyfastbss_core.py:
    It includes all the improved fastica algorithms and fastica algorithm.
    meica: multi-level extraction
    cdica: component dependent
    aeica: adaptive extraction
    ufica: aeica + cdica

    In this paper, we focus on MeICA, which improves the speed/reliability of AeICA, since AeICA highly depends on the initial extraction interval mu_0. 
All methods are based on FastICA.

# Other required packages:
    numpy \ scipy \ museval \ progressbar2

# To be done:
    1. Select the test data set: Google Audio Data Set or MUSDB18?
    2. Preparing test data set: length, sampling rate.
    3. Plot: confidential interval.
    4. Mathematical explanation: talk with the student first (Huan)
    5. Section Introduction writing