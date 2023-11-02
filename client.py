# Importação das bibliotecas (ambas são nativas)
import socket
import threading

# IP do localhost e porta de conexão
HOST = '127.0.0.1'
PORT = 6667

# Verirfica se o nickname esta dentro do limite
while True:
    nickname = input("Digite seu nome de usuário: ")
    if len(nickname) <= 9:
        break
    
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'USERNAME':                                                                                            
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            print("Encerrando conexão com o servidor...")
            client.close()
            break

def write():
    while True:
        try:
            message =  input("")
            client.send(message.encode('utf-8'))
        except KeyboardInterrupt:
            break

receive_thread = threading.Thread(target=receive)
receive_thread.start()
write()
