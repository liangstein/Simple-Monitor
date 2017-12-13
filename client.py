import os
import time
def client_monitor():
    list_gpu=os.popen("nvidia-smi --query-gpu=index,timestamp,power.draw,temperature.gpu,clocks.sm,clocks.mem,clocks.gr --format=csv")
    list_cpu=os.popen("sensors")
    hostname=os.popen("hostname")
    list_gpu=list_gpu.read()
    list_cpu=list_cpu.read()
    hostname=hostname.read()
    gpu_info=list_gpu.split("\n")[1:-1]
    number_of_gpus=len(gpu_info)
    gpu_temps=[]
    for i in range(number_of_gpus):
        ele=gpu_info[i].split(",")
        gpu_temps.append(float(ele[3]))
    gpu_states=""
    for i in range(number_of_gpus):
        if gpu_temps[i]<=75:
            gpu_states="ok"
        else:
            gpu_states="no"
            break
    result="Hostname: "+hostname+"\n"+"CPU states:\n"+list_cpu+"\n"+"GPU states:\n"+list_gpu+"\n"
    return result,gpu_states,hostname

def client_main(dir):
    while 1:
        monitor_result=client_monitor()
        host_name=monitor_result[-1].replace("\n","")
        with open(dir+str(host_name),"w") as f:
            f.write(str(monitor_result[0])+str(monitor_result[1]))
        time.sleep(5)

if __name__=="__main__":
    dir=os.getcwd()
    client_main(dir+"/hosts_data/")