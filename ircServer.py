import time
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
nicknames = []

channels = {
    "#cn1": []
}


def verificaComando(message):
    comando = message[0]
    if comando == "/":
        return True
    else:
        return False

def executaComando(client, message):

    comando = message.split(" ", 2)

    if comando[0] == "/privmsg" or comando[0] == "/msg":
        user = comando[1]
    
        for key in usuarios:
            if usuarios[key] == user:
                key.send(f"PRIVMSG {usuarios[client]}: {comando[2]}".encode('utf-8'))
                break
        
    if comando[0] == "/quit" or comando[0] == "/q":
        if client in usuarios:

            # Remove o usuário da lista de usuários
            nickname = usuarios.pop(client)
            nicknames.remove(nickname)


            client.close()

            sendMessage(f"{nickname} desconectou-se do servidor.".encode('utf-8'), client)

    if comando[0] == "/list" or comando[0] == "/l":
        client.send("Lista de usuários conectados: \n".encode('utf-8'))
        for key in usuarios:
            client.send(f"- {usuarios[key]}".encode('utf-8'))


def sendMessage(message, usr_client):
    try:
        for client in usuarios:
            if client and client != usr_client:
                client.send(message)
    except:
        print("Erro ao enviar mensagem.")

def handle(client, nickname):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if verificaComando(message):
                executaComando(client, message)
            else:
                sendMessage(f"{nickname}: {message}".encode('utf-8'), client)
        except:
            # Remove o usuário da lista de usuários
            if client in usuarios:
                nickname = usuarios.pop(client)
                nicknames.remove(nickname)
                sendMessage(f"{nickname} desconectou-se do servidor.".encode('utf-8'), client)

            client.close()

            break

def receive():
    while True:
        client, address = irc.accept()
        client.send("USERNAME".encode('utf-8'))

        nickname = client.recv(1024).decode('utf-8')
 
        if nickname in nicknames:
            client.send("NICKNAME_ALREADY_EXISTS".encode('utf-8'))
            client.close()
            
        else:
            client.send('NICKNAME_AVAILABLE'.encode('utf-8'))

            # Adiciona o usuário na lista de usuários
            usuarios[client] = nickname
            # Adiciona o nickname na lista de nicknames
            nicknames.append(nickname)

            print(f"O usuário {nickname} se conectou no servidor! Endereço: {address}")
            sendMessage(f"{nickname} entrou no chat.".encode('utf-8'), client)
            client.send('Conectado ao servidor!'.encode('utf-8'))
                            
            thread = threading.Thread(target=handle, args=(client, nickname, ))
            thread.start()

receive()