# Importação das bibliotecas (ambas são nativas)
import socket
import threading

# AF_INET -> Responsável pelo endereçamento IP
# SOCK_STREAM -> Responsável pela chamada do protocolo, nesse caso TCP
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# IP do localhost e porta de conexão
HOST = '127.0.0.1'
PORT = 6667

# Associa o HOST a porta PORT e em seguida fica "escutando" por chamados
irc.bind((HOST, PORT))
irc.listen()
print(f"Servidor IRC esperando por conexões em {HOST}:{PORT}...")

clients = []
nicknames = []

def sendMessage(message):
    for client in clients:
        client.send(message)

def handle(client, nickname):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            sendMessage(f"{nickname}: {message}".encode('utf-8'))
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            sendMessage(f"{nickname} desconectou-se do servidor.".encode('utf-8'))
            break

def receive():
    while True:
        client, address = irc.accept()
        client.send("USERNAME".encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
 
        print(f"O usuário {nickname} se conectou no servidor! endereço: {address}")
        sendMessage(f"{nickname} entrou no chat.".encode('utf-8'))
        clients.append(client)
        client.send('Conectado ao servidor!'.encode('utf-8'))
                    	
        thread = threading.Thread(target=handle, args=(client, nickname, ))
        thread.start()

receive()