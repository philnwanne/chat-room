from http import server
import threading
import socket

# for a web server ensure to change the local host address to the address of your server
host = '127.0.0.1' # localhost

# try not to choose reserved ports 
port = 33500

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port)) # here we need to bind the server to the local host's address
server.listen() # then put our server into listening mode to pick up incoming connections

# Now let's define a couple of methods

clients = [] # initiate an empty list to store all our clients
nicknames = [] # an empty list to get a nickname for a client

# function/method for a server to broadcast a message to all the clients that are connected to it
def broadcast(message):
    for client in clients:
        client.send(message)

# recieve message if a client comes online and sends a message then broadcast the message to all other clients 
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat-room'.encode('ascii'))
            nicknames.remove(nickname)
            break

# to receive client connections via the accept method
def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}!')
        broadcast(f'{nickname} joined the chat!'.encode('ascii'))
        client.send('You are now connected to the server!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start

print(f'Server is listening on port {port}...')
receive()
 


