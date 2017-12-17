import os
import pickle
import numpy as np
from datetime import datetime
from flask import  Flask,Response
app=Flask(__name__)
main_dir="/opt/simple_monitor/"

@app.after_request
def treat_as_plain_text(response):
    response.headers["content-type"] = "text/plain"
    return response

@app.route("/")
def index():
    hosts = os.listdir(main_dir + "/hosts_data/")
    normal_states_string = ""
    caution_states_string=""
    now=datetime.now()
    year=now.year
    month=now.month
    day=now.day
    hour=now.hour
    minute=now.minute
    second=now.second
    now_time=str(year) + str(month) + str(day) + str(hour) + str(minute) + str(second)
    lost_nodes=[]
    gpu_warning_location = {}
    for host in hosts:
        gpu_warning_list=[]
        with open(main_dir+"/hosts_data/"+str(host),"rb") as f:
            gpu_states=pickle.load(f)
        normal_states_string+=str(host)+":\n"
        for i in gpu_states:
            if i!="time":
                normal_states_string+=str(i)+": "+str(gpu_states[i])+"\n"
                gpu_temp=gpu_states[i][-1]
                if gpu_temp>65:
                    gpu_warning_list.append((str(i),str(gpu_states[i])))
        node_time=gpu_states["time"]
        if abs(float(node_time)-float(now_time))>200:
            lost_nodes.append(host)
        if len(gpu_warning_list)!=0:
            gpu_warning_location[host]=gpu_warning_list
        normal_states_string+="\n"
    if len(gpu_warning_location)!=0:
        caution_states_string+="Caution! Following GPUs are too hot:\n"
        for i in gpu_warning_location:
            caution_states_string+=str(i)+str(gpu_warning_location[i])+"\n"
    if len(lost_nodes)!=0:
        caution_states_string+="Caution! Following nodes are disconnected:\n"
        for i in lost_nodes:
            caution_states_string+=str(i)+"\n"
    return  normal_states_string+caution_states_string

if __name__=="__main__":
    app.run(debug=1,host='0.0.0.0',port=8002)