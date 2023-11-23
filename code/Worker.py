import zmq
import time
import json
import ProjectCore
from math import *
def worker(Port):
    print('Starting worker on Port: ', Port)
    con = "tcp://*:" + Port
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(con)
    message = socket.recv_json()
    ProjectCore.main()
    socket.send_json("done")
    return 0



