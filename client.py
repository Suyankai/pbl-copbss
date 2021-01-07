from pyfastbss_core import PyFastbss, pyfbss
from pyfastbss_testbed import pyfbss_tb
import pyfastbss_example as pyfbss_ex
import numpy as np
import os
import sys
import math
import argparse
import progressbar
# 引用一些hop节点
from hop_B_Manager import hop_B_Manager
from hop_MeICA_controller import hop_MeICA_controller
import hop_MeICA_newton_iteration
from hop_Source_controller import hop_Source_controller
# 画图
import matplotlib.pyplot as plt
import matplotlib as mpl


PGB = progressbar.ProgressBar()


# init parameter to generate S
source_number = 5
mixing_type = "normal"
max_min = (1, 0.01)
mu_sigma = (0, 1)
folder_address = 'google_dataset/32000_wav_factory'
duration = 3

# 用于输出结果的参数
tmp_meica = [source_number]
Eve_MeICA = []

#参数 MeICA
max_iter = 100
tol = 1e-04,
break_coef = 0.92
ext_multi_ica = 2


def init_arg():

    parser = argparse.ArgumentParser(description='Setting for Client')

    # MeICA的循环节点时间
    parser.add_argument(
        "--iter_time",
        type=int,
        default=[0, 0],
        nargs=2,
        choices=[0, 1],
        help="get meantime of iteration and plot eachtime and iter num, default [0,0]",
    )


    # 是否运算fastICA
    parser.add_argument(
        "--run_FastICA",
        action='store_true',
        help="run FastICA",
    )

    # mircoservice和origin比较
    parser.add_argument(
        "--run_MeICA",
        action='store_true',
        help="run MeICA",
    )

    # Simulator
    parser.add_argument(
        "--run_Simulator",
        action='store_true',
        help="run time Simulator, it will simulate the time base on our microsevice, you can setting the latency and performance for simulator, see help",
    )

    # 设定默认source个数
    parser.add_argument(
        "--source_num",
        type=int,
        default=5,
        help="setting source number, default: 5",
    )

    parser.add_argument(
        "--service_latency",
        type=float,
        default=50,
        help="setting the latency of service for origin MeICA, default:50[ms]"
    )

    parser.add_argument(
        "--service_performance",
        type=int,
        default=10,
        help="setting the performance of service compare to mircoservice, default:10x "
    )

    parser.add_argument(
        "--micro_latency",
        type=float,
        default=0.5,
        help="setting the latency of micro service, default:0.5[ms]"
    )
    args = parser.parse_args()
    return args

def run_ms():
    print(f'Run MeICA base mircoservice, source number:{source_number}')
    Source_controller = hop_Source_controller(
        folder_address, duration, source_number, mixing_type, max_min, mu_sigma)
    B_Manager = hop_B_Manager(Source_controller)
    MeICA_controller = hop_MeICA_controller(
        max_iter, tol, break_coef, ext_multi_ica, Source_controller, B_Manager)
    hat_S = MeICA_controller.get_hat_S()
    runtime_list = MeICA_controller.get_runtime_list()
    grad = MeICA_controller.get_grad()
    iter_list = MeICA_controller.get_iter_list()
    # 写入文件
    ad_work=os.getcwd()
    os.chdir("./test_results/naibao_result/")
    ms_res=open("iter_info.txt","w")
    # 打印节点信息
    ms_res.write('-------------Hop Usage:--------------\n')
    ms_res.write('hop_MeICA_Controller:          1\n'
         +'hop_Source_controller:         1\n'
         +'hop_B_Manager:                 1\n'
         +f'hop_MeICA_newton_iteration:    {grad}\n')
    ms_res.write('-------------------------------------\n')
    ms_res.write(f'Totol Hop:                     {3+grad}\n')    
    # 打印iteration迭代信息
    ms_res.write('------------Info Iteration-----------\n')
    ms_res.write('-------------------------------------\n')
    ms_res.write('hop           time[ms]       iter_num\n')
    for hop_i in range(grad):
        ms_res.write(f'{hop_i+1:2}            {runtime_list[hop_i]*1000:8.4f}        {iter_list[hop_i]:<}\n')
    ms_res.write('-------------------------------------\n')
    ms_res.write(f'Meantime[ms]                 {np.mean(np.array(runtime_list))*1000:8.4f}\n')
    ms_res.close()
    os.chdir(ad_work)
    print('finish!\nplease check ./test_results/naibao_result/iter_info.txt')

def run_plot(if_fast:bool,if_me:bool,if_simu:bool,latency_ms,latency_serv,performance):
    eval_type = 'sdr'
    # 设定x axis
    source_list=[]
    # 设定 ms_MeICA
    time_list_ms_MeICA=[]
    snr_list_ms_MeICA=[]
    # 设定 Me_ICA
    time_list_MeICA=[]
    snr_list_MeICA=[]    
    # 设定 Fast_ICA
    time_list_FastICA=[]
    snr_list_FastICA=[]
    for s in PGB(range(2,source_number+1,1)):
        print(f'starting for source_number:{s}')
        print('running Ms_MeICA...')
        source_list.append(s)
        Source_controller = hop_Source_controller(
            folder_address, duration, s, mixing_type, max_min, mu_sigma)
        B_Manager = hop_B_Manager(Source_controller)
        # use same init B
        B_init=B_Manager.get_B()
        
        # Part MS_MeICA
        pyfbss_tb.timer_start()
        MeICA_controller = hop_MeICA_controller(
            max_iter, tol, break_coef, ext_multi_ica, Source_controller, B_Manager)
        hat_S_ms = MeICA_controller.get_hat_S()
        time_ms_MeICA=pyfbss_tb.timer_value()
        # Time simulator
        if if_simu:
            # reset time for ms_MeICA
            # 算法：
            # client发送接受Source_Controller和B_Manager的信息，latency*4
            # client将信息发送MeICA_Controller最后接受S，latency*2
            # MeICA_Controller接受B，最后更新B，latency*2*(grad+1)
            # MeICA_Controller发送接收B_temp到iter,latency*2*(grad+1)
            time_ms_MeICA=time_ms_MeICA+(4+2+4*MeICA_controller.get_grad()+4)*latency_ms
        
        time_list_ms_MeICA.append(time_ms_MeICA)
        snr_list_ms_MeICA.append(pyfbss_tb.bss_evaluation(
            Source_controller.get_S(), hat_S_ms, eval_type)) 
        
        # Part FastICA
        if if_fast:
            print('running FastICA...')
            pyfbss_tb.timer_start()
            X=Source_controller.get_X()
            X, V = pyfbss.whiten(X)
            B1 = B_init
            B2 = pyfbss.newton_iteration(B1, X, max_iter, tol)[0]
            hat_S_Fast = np.dot(B2, X)
            time_Fast=pyfbss_tb.timer_value()
            
            # Time Simulator
            if if_simu:
                # 算法：
                # 中间的运算时间根据性能比线性缩短，之后latency*2
                time_Fast=time_Fast/performance+latency_serv*2
                pass

            time_list_FastICA.append(time_Fast)
            snr_list_FastICA.append(pyfbss_tb.bss_evaluation(Source_controller.get_S(), hat_S_Fast, eval_type))
            
        # Part MeICA
        if if_me:
            print('running MeICA...')
            pyfbss_tb.timer_start()
            X=Source_controller.get_X()
            pyfbss.Stack = []
            B1 = B_init
            B2 = pyfbss.multi_level_extraction_newton_iteration(
            X, B1, max_iter, tol, break_coef, ext_multi_ica)
            hat_S_MeICA = np.dot(B2, X)
            time_MeICA=pyfbss_tb.timer_value()
            # Time Simulator
            if if_simu:
                # 算法和FastICA一样
                time_MeICA=time_MeICA/10+latency_serv*2
            time_list_MeICA.append(time_MeICA)
            snr_list_MeICA.append(pyfbss_tb.bss_evaluation(Source_controller.get_S(), hat_S_MeICA, eval_type))
        
    # plot
    plt.figure()
    plt.subplot(1,2,1)
    plt.plot(np.array(source_list),np.array(time_list_ms_MeICA),'o-',label='MircoService_MeICA')
    if if_fast:
        plt.plot(np.array(source_list),np.array(time_list_FastICA),'o-',label='FastICA')
    if if_me:
        plt.plot(np.array(source_list),np.array(time_list_MeICA),'o-',label='MeICA')
    plt.title(f'Time Use, base on Simulator:{if_simu}')
    plt.xlabel('Source Number')
    plt.ylabel('Time[ms]')
    # 添加图例
    plt.legend(loc='best')

    plt.subplot(1,2,2)
    plt.plot(np.array(source_list),np.array(snr_list_ms_MeICA),'o-',label='MircoService_MeICA')
    if if_fast:
        plt.plot(np.array(source_list),np.array(snr_list_FastICA),'o-',label='FastICA')
    if if_me:
        plt.plot(np.array(source_list),np.array(snr_list_MeICA),'o-',label='MeICA')
    plt.title(f'SNR')
    plt.xlabel('Source Number')
    plt.ylabel('SNR[dB]')
    # 添加图例
    plt.legend(loc='best')
    plt.show()


if __name__ == "__main__":
    # 接受命令
    args = init_arg()

    if_fast = args.run_FastICA
    if_me = args.run_MeICA
    if_mean = args.iter_time[0]
    if_plot = args.iter_time[1]
    if_simu = args.run_Simulator
    source_number=args.source_num

    latency_ms = args.micro_latency
    latency_serv = args.service_latency
    performance = args.service_performance
    # 获取迭代参数
    if if_mean:
        run_ms()
    
    # 画出对比图形
    run_plot(if_fast,if_me,if_simu,latency_ms,latency_serv,performance)