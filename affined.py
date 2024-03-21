import socket
import numpy as np
import time
from   multiprocessing import Pool
import os

def send_message(k):
    message, client, affinity_mask = tuple(k)
    os.sched_setaffinity(os.getpid(), affinity_mask)
    emessage = bytes(str(message), 'utf-8')
    client.send(emessage)
    data = client.recv(1024)
    if data:
        return data

def server(HOST, PORT, messages, t):
    
    pool = Pool(processes=t-1)
    cpu_count = os.cpu_count() - 1
    
    with Pool(processes=t-1) as pool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            while True:
                
                conn, addr = s.accept()
                if conn not in config:
                    config.append(conn)
                if len(config) == t-1:
                    d = []
                    am = 0
                    for i in range(t-1):
                        am += 1
                        if am > cpu_count:
                            am = 1
                        d.append([messages[i], config[i], {am}])
                    for repeat in range(3):
                        res = []
                        threads = [None] * (t-1)
                        time_before = time.time()
                        with Pool(processes=t-1) as pool:
                            res.append(pool.map(send_message, d))
                            
                        time_after = time.time()
                        print (f"{time_after - time_before}")
                    break
                        # for i in range(t-1):

                        #     threads[i] = pool.apply_async(send_message, args=(d[i][0], d[i][1],d[i][2]))
                        # for i in range(t-1):
                        #     res.append(threads[i].get())
                            
            

def client(HOST, PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        cnt = 0
        while True:
            data = s.recv(1024)
            
            if data:
                cnt += 1
                time_before = time.time()
                emessage = bytes("ACK!", 'utf-8')
                s.send(emessage)
                time_after = time.time()
                print (f"{time_after - time_before}")
                if cnt == 3:
                    break

            
        
        
res = []
s = int(input("s = "))
N = [2000]
T = [3]
master_ip = '10.0.4.192'
master_port = 7000
config = []



if s == 0:
    for n in N:
        M = np.random.randint(0,100,size = (n,n))
        for t in T:
            m = np.array_split(M, t)
            for repeat in range(1):
                server(master_ip, master_port, m, t)
                
elif s == 1:
    client(master_ip, master_port)
    




