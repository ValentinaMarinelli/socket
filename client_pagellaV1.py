import socket
import json

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5005
BUFFER_SIZE = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((SERVER_IP,SERVER_PORT))
    print("Comandi utilizzabili: ")
    print('#list (voti inseriti) \n #get /nomestudente (voti di uno studente) \n #set /nomestudente (inserire studente) \n #put /nomestudente/materia/voto/ore (aggiungere voti materia studente) \n #close (chiudere connessione)')
    while True:
        comando = (input("Inserisci un comando: "))
        if (comando != "#close" and comando != "#list"):
            parametro = (input("Inserisci nome di uno studente, con / : "))
        elif(comando == "#close"):
            parametro = " "
            break
        else:
            parametro = " "
        messaggio = {
            "comando":comando,
            "parametro":parametro,
        }
        messaggio=json.dumps(messaggio) 
        sock.sendall(messaggio.encode("UTF-8"))
        dati=sock.recv(BUFFER_SIZE)
        
        ris = json.loads(dati.decode())
        print(ris['risultato'])
