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

usuarios = {}

clients = []
nicknames = []

def verificaComando(message):
    comando = message[0]
    if comando == "/":
        return True
    else:
        return False

def executaComando(message):

    comando = message.split(" ")

    if comando[0] == "/quit":
        index = clients.index(client)
        clients.remove(client)
        client.close()
        nickname = nicknames[index]
        nicknames.remove(nickname)
        sendMessage(f"{nickname} desconectou-se do servidor.".encode('utf-8'))

    if comando[0] == "/list":
        sendMessage("Lista de usuários conectados: \n".encode('utf-8'))
        for key in usuarios:
            sendMessage(f"- {usuarios[key]}\n".encode('utf-8'))
        # for nickname in nicknames:
        #     sendMessage(f"- {nickname}\n".encode('utf-8'))

def sendMessage(message):
    for client in clients:
        client.send(message)

def handle(client, nickname):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if verificaComando(message):
                executaComando(message)
            else:
                sendMessage(f"{nickname}: {message}".encode('utf-8'))
        except:
            #
            usuarios.pop(client)
            #
            print(f"Usuários: {usuarios}")
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
 
        #
        usuarios[client] = nickname
        #

        print(usuarios)

        print(f"O usuário {nickname} se conectou no servidor! Endereço: {address}")
        sendMessage(f"{nickname} entrou no chat.".encode('utf-8'))
        clients.append(client)
        client.send('Conectado ao servidor!'.encode('utf-8'))
                    	
        thread = threading.Thread(target=handle, args=(client, nickname, ))
        thread.start()

receive()