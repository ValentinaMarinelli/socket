import socket
import json

#Configurazione del server
IP = "127.0.0.1"
PORTA = 5005
DIM_BUFFER = 1024

#Creazione della socket del server con il costrutto with
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_server:
  sock_server.bind((IP,PORTA))
  sock_server.listen()
  print(f"Server in ascolto su {IP}:{PORTA}...")
  while True:
    #Accetta le connessioni
    sock_service,address_client = sock_server.accept()
    with sock_service as sock_client:
      #Leggi i dati inviati dal client
      dati = sock_client.recv(DIM_BUFFER).decode()
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

      ris = str(risultato)
      sock_service.sendto(ris.encode(),address_client)