from pyfastbss_core import PyFastbss, pyfbss
from pyfastbss_testbed import pyfbss_tb
import pyfastbss_example as pyfbss_ex
import numpy as np
import os
import math
import progressbar
import socket
PGB = progressbar.ProgressBar()


def init_B(X):
    """
    # 初始化一个B和lim
    """
    B = pyfbss.generate_initial_matrix_B(X)
    lim = None
    pass

def update_B(B_get,lim_get,B,lim):
    """
    # 根据lim的大小来保持最优的B和lim
    """
    if (lim_get<lim | lim==None):
        return B_get, lim_get
    else:
        return B,lim

if __name__ == "__main__":
    # socket 
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    port = 12300
    s.bind(('localhost',port))
    
    s.listen(5)

    while True:
        c,addr=s.accept()
        

    # TODO: 接受controller的X,生成B

    # 这个节点用来处理B矩阵，首先生成一个初始化的B
    X=0
    

    # TODO 接受信号 B,Lim 并和目前的B, Lim
    pass