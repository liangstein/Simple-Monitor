# Simple-Monitor
An easily designed cluster monitor.
## Requirements: 
Python with Flask
## Usage:
Run client.py on each node, then run http_server.py on the master node.
This tool is mainly used for monitoring GPU clusters. It can print items like power draws and temperatures on a web page. It can give warnings of GPUs within too high temperatures and warnings of nodes that are disconnected from the monitoring server. 
