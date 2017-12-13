import os
import time
def client_monitor():
    list_gpu=os.popen("nvidia-smi --query-gpu=index,timestamp,power.draw,temperature.gpu,clocks.sm,clocks.mem,clocks.gr --format=csv")
    list_cpu=os.popen("sensors")
    hostname=os.popen("hostname")
    list_gpu=list_gpu.read()
    list_cpu=list_cpu.read()
    hostname=hostname.read()
    #result="\n".join(str(k) for k in list)
    result="Hostname: "+hostname+"\n"+"CPU states:\n"+list_cpu+"\n"+"GPU states:\n"+list_gpu+"\n"
    return result,hostname

def client_main(dir):
    while 1:
        monitor_result=client_monitor()
        host_name=monitor_result[-1].replace("\n","")
        with open(dir+str(host_name),"w") as f:
            f.write(str(monitor_result[0]))
        time.sleep(5)

if __name__=="__main__":
    dir=os.getcwd()
    client_main(dir+"/hosts_data/")