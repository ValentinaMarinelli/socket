import socket
import json
from threading import Thread

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 5005
BUFFER_SIZE = 2048

def ricevi_comandi(sock,addr_client):
    print("In attesa di comandi da ", addr_client)
    with sock as sock_client:
        while True:
        #Leggi i dati inviati dal client
            dati = sock_client.recv(BUFFER_SIZE).decode()
            if not dati:
                break
            dati = json.loads(dati)
            primoNumero = dati['primoNumero']
            operazione = dati['operazione']
            secondoNumero = dati['secondoNumero']
                    
            risultato = 0
            if(operazione=="+"):
                risultato = primoNumero+secondoNumero
            elif(operazione=="-"):
                risultato = primoNumero-secondoNumero
            elif(operazione=="*"):
                risultato = primoNumero*secondoNumero
            elif(operazione=="/"):
                if(secondoNumero!=0):
                    risultato = primoNumero/secondoNumero
                else:
                    print("La divisione per 0 non può essere eseguita!")
            elif(operazione=="%"):
                    risultato = primoNumero%secondoNumero

            risultato = str(risultato)
            print(risultato, type(risultato))
            sock_client.sendall(risultato.encode())
        sock_client.close()

def ricevi_connessioni(sock_listen):
    print("Server in attesa di connessioni...")
    while True:
        sock_service, addr_client = sock_listen.accept()
        print("\nConnessione ricevuta da %s" % str(addr_client))
        print("Creo un thread per servire le richieste")
        try:
            Thread(target=ricevi_comandi,args=(sock_service,addr_client)).start()
        except:
            print("Il thread non si avvia")
            sock_listen.close()

def avvia_server(indirizzo,porta):
    try:
        sock_listen = socket.socket()
        sock_listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        sock_listen.bind((indirizzo,porta))
        sock_listen.listen(5)
        ricevi_connessioni(sock_listen)
        print("Server avviato")
    except socket.error as errore:
        print("Errore riscontrato", errore)
    

if __name__ == '__main__':
    avvia_server(SERVER_ADDRESS, SERVER_PORT)

print("Termina")
