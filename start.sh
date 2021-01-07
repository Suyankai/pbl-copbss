export DISPLAY=`cat /etc/resolv.conf | grep nameserver | awk '{print $2}'`:0
python3 client.py --run_FastICA --run_MeICA --run_Simulator