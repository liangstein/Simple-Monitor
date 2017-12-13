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
    for host in hosts:
        with open(main_dir + "hosts_data/" + host, "r") as f:
            node_states = f.read()
        total_states_string += node_states
    return  total_states_string

if __name__=="__main__":
    app.run(debug=1,host='0.0.0.0',port=8002)