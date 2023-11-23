import threading
import time
import zmq
import json
import numpy as np
import pandas as pd
import Worker
t=0

print ('Ready to go')
def saveList(myList,filename):
    # the filename should mention the extension 'npy'
    np.save(filename,myList)
    #print("Saved successfully!")
def loadList(filename):
    # the filename should mention the extension 'npy'
    tempNumpyArray=np.load(filename)
    return tempNumpyArray.tolist()
portlist=[['5555',0]]
saveList(portlist,'portlist.npy')
def aWorker_asRoutine( aWorker_URL, t,aContext = None ):
    """Worker routine"""
    #Context to get inherited or create a new one trick------------------------------
    aContext = aContext or zmq.Context.instance()

    # Socket to talk to dispatcher --------------------------------------------------
    socket = aContext.socket( zmq.REP )

    socket.connect( aWorker_URL )

    while True:
        temp = socket.recv()

        count = 0
        for i in range(len(portlist)):
            if portlist[i][1] == '0':
                portlist[i][1] = '1'
                Port = portlist[i][0]
                count = 1
                break
        if count == 0:
            Port = str(int(portlist[len(portlist) - 1][0]) + 1)
            if int(Port) >= 5655:
                Port = "5555"
            portlist.append([Port, 1])

        connection = "tcp://localhost:" + Port
        contexts[t] = zmq.Context()
        sockets[t] = contexts[t].socket(zmq.REQ)
        sockets[t].connect(connection)
        sockets[t].send_json("start the worker")
        Worker.worker(Port)
        messages[t] = sockets[t].recv()
        #print(messages[t])
        saveList(portlist, 'portlist.npy')
        #time.sleep(3)
        #print(t)
        for i in range(len(portlist)):
            if portlist[i][0] == Port:
                portlist[i][1] = '0'
                saveList(portlist, 'portlist.npy')
                break
        socket.send_json("ok")
def main(t):
    """Server routine"""

    url_worker = "inproc://workers"
    url_client = "tcp://*:1048"

    # Prepare our context and sockets ------------------------------------------------
    aLocalhostCentralContext = zmq.Context.instance()

    # Socket to talk to clients ------------------------------------------------------
    clients = aLocalhostCentralContext.socket( zmq.ROUTER )
    clients.bind( url_client )

    # Socket to talk to workers ------------------------------------------------------
    workers = aLocalhostCentralContext.socket( zmq.DEALER )
    workers.bind( url_worker )

    # Launch pool of worker threads --------------< or spin-off by one in OnDemandMODE >
    for i in range(10):
        t=t+1
        thread = threading.Thread( target = aWorker_asRoutine, args = ( url_worker,t , ) )
        thread.start()

    zmq.device( zmq.QUEUE, clients, workers )

    # clean up
    clients.close()
    workers.close()
    aLocalhostCentralContext.term()

if __name__ == "__main__":
    sockets={}
    contexts={}
    messages={}
    portlist = loadList('portlist.npy')
    main(t)
