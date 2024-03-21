import socket
import numpy as np
import time

def server(HOST, PORT, messages, t):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            if conn not in config:
                config.append(conn)
            if len(config) == t-1:
                for repeat in range(3):
                    time_before = time.time()
                    for i in range(t-1):
                        emessage = bytes(str(messages[i]), 'utf-8')
                        config[i].send(emessage)
                        data = config[i].recv(1024)
                        if data:
                            res.append(data)
                    time_after = time.time()
                    print (f"{time_after - time_before}")
                break    
        

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
            
        
        

s = int(input("s = "))
N = [2000]
T = [3]
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
    




