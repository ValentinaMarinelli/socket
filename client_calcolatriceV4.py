import socket
import sys
from random import *
import os
import time
import threading
import multiprocessing
import json

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 5005
NUM_WORKERS = 15
BUFFER_SIZE = 2048

def genera_richieste(SERVER_ADDRESS, SERVER_PORT):
    try:
        start_time_thread = time.time()
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((SERVER_ADDRESS,SERVER_PORT))
    except:
        print(f"{threading.current_thread().name} non si connette")
    primoNumero = randint(1,15)
    operazioni = ["+","-","*","/","%"]
    num = randint(0,4)
    operazione = operazioni[num]
    secondoNumero = randint(1,15)
    messaggio = {'primoNumero' : primoNumero,
                'operazione' : operazione,
                'secondoNumero' : secondoNumero}
    messaggio = json.dumps(messaggio)
    s.sendall(messaggio.encode("UTF-8"))
    data = s.recv(BUFFER_SIZE)
    print("Risultato: ", data.decode())
    end_time_thread = time.time()
    print(f"{threading.current_thread().name} execution time =", end_time_thread-start_time_thread)

if __name__ == '__main__':
    start_time = time.time()
    threads = [threading.Thread(target=genera_richieste,args=(SERVER_ADDRESS,SERVER_PORT,)) for _ in range(NUM_WORKERS)]
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]
    end_time = time.time()

    print("Total threads time = ", end_time-start_time)