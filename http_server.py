import os
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
    total_states_string = ""
    gpu_temp_check_list=[]
    for host in hosts:
        with open(main_dir + "hosts_data/" + host, "r") as f:
            node_states = f.read()
        total_states_string += node_states[:-2]
        gpu_temp_check_list.append(node_states[-2:])
    gpu_warning=""
    for i in range(len(gpu_temp_check_list)):
        if gpu_temp_check_list[i]!="ok":
            gpu_warning="There is at least one GPU too hot on "+str(hosts[i])
        else:
            gpu_warning="All GPUs are in proper temperature conditions! "
    return  total_states_string+"\n"+gpu_warning+"\n"

if __name__=="__main__":
    app.run(debug=1,host='0.0.0.0',port=8002)