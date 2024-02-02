import socket
import json

#Configurazione del server
IP = "127.0.0.1"
PORTA = 5005
DIM_BUFFER = 1024

diz = {'Antonio Barbera': [['Matematica', 8, 1],
                           ['Italiano', 6, 1],
                           ['Inglese', 9.5, 0],
                           ['Storia', 8, 2],
                           ['Geografia', 8, 1]],
        'Giuseppe Gullo': [['Matematica', 9, 0],
                           ['Italiano', 7, 3],
                           ['Inglese', 7.5, 4],
                           ['Storia', 7.5, 4],
                           ['Geografia', 5, 7]],
        'Nicola Spina':   [['Matematica', 7.5, 2],
                           ['Italiano', 6, 2],
                           ['Inglese', 4, 3],
                           ['Storia', 8.5, 2],
                           ['Geografia', 8, 2]]}

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_server:
  sock_server.bind((IP,PORTA))
  sock_server.listen()
  print(f"Server in ascolto su {IP}:{PORTA}...")
  while True:
    sock_service,address_client = sock_server.accept()
    print(f"Connessione avviata con {address_client}")
    with sock_service as sock_client:
        while True:
            dati = sock_client.recv(DIM_BUFFER).decode()
            if not dati:
                break
            dati = json.loads(dati)
            comando = dati['comando']
            parametro = dati['parametro']
            
            if(comando == "#list"):
               print("Dizionario studenti: ")
               risposta ="OK"
               risultato = diz
            elif(comando == "#get"):
               nome = parametro.split("/")[1]
               if(nome in diz):
                  risposta = "OK"
                  risultato = diz[nome]
               else:
                  risultato = "Studente non presente"
                  risposta = "KO"
            elif(comando == "#set"):
               nome = parametro.split("/")[1]
               if(nome in diz):
                  risposta = "KO"
                  risultato = "Studente già presente"
               else:
                  diz[nome] = []
                  risultato = "Inserimento in corso..." + "Studente inserito"
                  risposta = "OK"
            elif(comando == "#put"):
               nome = parametro.split("/")[1]
               materia = parametro.split("/")[2]
               voto = parametro.split("/")[3]
               ore = parametro.split("/")[4]
               if(nome in diz):
                  diz[nome]=[materia, voto, ore]
                  risposta = "OK"
                  risultato = "Dati aggiunti"
               else:
                  risultato = "Studente non presente"
                  risposta = "KO"
            else:
               print("Connessione terminata")
               sock_service.close()


            dati = {"risposta" : risposta,
                    "risultato" : risultato,
            }
            print(dati)
            
            sock_service.sendall(json.dumps(dati).encode())
    