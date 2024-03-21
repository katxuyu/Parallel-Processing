import socket
import numpy as np
import time
from   multiprocessing import Pool
from   multiprocessing.pool import ThreadPool
import os

def send_message(message, client):
    emessage = bytes(str(message), 'utf-8')
    client.send(emessage)
    data = client.recv(1024)
    #print(data)
    if data:
        return res.append(data)

def server(HOST, PORT, messages, t):
    threads = [None] * (t-1)
    pool = ThreadPool(processes=t-1)
    cpu_count = os.cpu_count() - 1
    am = 0
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            if conn not in config:
                config.append(conn)
            if len(config) == t-1:
                
                for i in range(t-1):
                    threads[i] = pool.apply_async(send_message, args=(messages[i], config[i]))
                time_before = time.time()
                for j in range(t-1):
                    res.append(threads[j].get())

                
                time_after = time.time()
                print (f"{time_after - time_before}")
                break    
        s.close()

def client(HOST, PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            data = s.recv(1024)
            if data:
                time_before = time.time()
                emessage = bytes("ACK!", 'utf-8')
                s.send(emessage)
                time_after = time.time()
                print (f"{time_after - time_before}")
                break

            
        
        

s = int(input("s = "))
N = [200]
T = [2]
master_ip = '127.0.0.1'
master_port = 23456
config = []
res = []


if s == 0:
    for n in N:
        M = np.random.randint(0,100,size = (n,n))
        for t in T:
            m = np.array_split(M, t)
            for repeat in range(1):
                server(master_ip, master_port, m, t)
                
elif s == 1:
    client(master_ip, master_port)
    




