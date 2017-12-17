import os
import time
import pickle
from datetime import datetime
def client_monitor():
    list_gpu=os.popen("nvidia-smi --query-gpu=gpu_name,index,power.draw,temperature.gpu --format=csv")
    #list_cpu=os.popen("sensors")
    hostname=os.popen("hostname")
    list_gpu=list_gpu.read()
    #list_cpu=list_cpu.read()
    hostname=hostname.read()
    now=datetime.now()
    year=now.year
    month=now.month
    day=now.day
    hour=now.hour
    minute=now.minute
    second=now.second
    gpu_info=list_gpu.split("\n")[1:-1]
    number_of_gpus=len(gpu_info)
    gpu_information={}
    repeat_count=1
    for i in range(number_of_gpus):
        ele=gpu_info[i].split(",")
        if i>0:
            if ele[0]!=gpu_info[i-1].split(",")[0]:
                gpu_information[ele[0]]=(float(ele[-2].replace("W","")),float(ele[-1]))
            else:
                gpu_information[ele[0]+" "+str(repeat_count)]=(float(ele[-2].replace("W","")),float(ele[-1]))
                repeat_count+=1
        else:
            gpu_information[ele[0]] = (float(ele[-2].replace("W", "")), float(ele[-1]))
    gpu_information["time"]=[year,month,day,hour,minute,second]
    return hostname,gpu_information

def client_main(dir):
    while 1:
        monitor_result=client_monitor()
        host_name=monitor_result[0].replace("\n","")
        with open(dir+str(host_name),"wb") as f:
            pickle.dump(monitor_result[-1],f,protocol=pickle.HIGHEST_PROTOCOL)
        time.sleep(5)

if __name__=="__main__":
    dir=os.getcwd()
    client_main(dir+"/hosts_data/")