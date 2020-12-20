import sys
from numpy.lib.utils import source
sys.path.append("..")
from pyfastbss_core import PyFastbss, pyfbss
from pyfastbss_testbed import pyfbss_tb
from hop_Source_controller import hop_Source_controller

import progressbar

PGB = progressbar.ProgressBar()


class hop_B_Manager:
    def __init__(self, Source_controller:hop_Source_controller) -> None:
        super().__init__()
        """
        # 初始化一个B和lim
        """
        self.B = pyfbss.generate_initial_matrix_B(Source_controller.get_X())
        self.lim = None
        
       

    def update_B(self,B,lim):
        """
        根据lim的大小来保持最优的B和lim
        
        """
        # 如果传进B只是中间的临时值，则传入lim为None，此时只更新B        
        if lim == None:
            self.B=B
        # 如果存在lim则进行对比
        else:
            if self.lim == None:
                self.B=B
                self.lim=lim
            elif self.lim>=lim:
                self.B=B
                self.lim=lim

            
        

    def get_B(self):
        return self.B

""" if __name__ == "__main__":
    # socket 
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    port = 12300
    s.bind(("127.0.0.1",port))
    
    s.listen(5)

    while True:
        c,addr=s.accept()
        

    # TODO: 接受controller的X,生成B

    # 这个节点用来处理B矩阵，首先生成一个初始化的B
    X=0
    

    # TODO 接受信号 B,Lim 并和目前的B, Lim
    pass """